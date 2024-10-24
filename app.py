import requests
import time
import os
import matplotlib.pyplot as plt
from datetime import datetime
from config import API_KEY, CITIES
import smtplib
import sqlite3
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template

# Email Configuration
EMAIL_ADDRESS = 'clashruban12@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'Ruban@180802'  # Replace with your email password

# Database Initialization
def init_db():
    conn = sqlite3.connect('weather_data.db')  # Create a database file
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather_summary (
            id INTEGER PRIMARY KEY,
            city TEXT,
            date DATE,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            humidity INTEGER,
            wind_speed REAL
        )
    ''')
    conn.commit()
    conn.close()

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather(city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'main': data['weather'][0]['main'],
            'temp': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'humidity': data['main']['humidity'],  # Added humidity
            'wind_speed': data['wind']['speed'],    # Added wind speed
            'dt': data['dt']
        }
        return weather_info
    else:
        return None

def fetch_weather_for_cities():
    weather_data = {}
    for city, city_id in CITIES.items():
        weather_info = get_weather(city_id)
        if weather_info:
            update_weather_summary(city, weather_info)
            check_alert(city, weather_info)
            weather_data[city] = weather_info  # Store the latest weather info
        else:
            print(f"Failed to fetch data for {city}")
        time.sleep(1)  # To avoid hitting the API rate limit
    print(weather_data)  # Debug output
    return weather_data

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_weather_for_cities, 'interval', minutes=5)
    scheduler.start()

weather_aggregate = {}

def update_weather_summary(city, weather_info):
    if city not in weather_aggregate:
        weather_aggregate[city] = {
            'temps': [],
            'dominant_conditions': {},
            'max_temp': None,
            'min_temp': None,
            'humidity': [],           # Added humidity tracking
            'wind_speed': []          # Added wind speed tracking
        }

    # Update temperature aggregates
    weather_aggregate[city]['temps'].append(weather_info['temp'])
    weather_aggregate[city]['humidity'].append(weather_info['humidity'])  # Store humidity
    weather_aggregate[city]['wind_speed'].append(weather_info['wind_speed'])  # Store wind speed

    if weather_aggregate[city]['max_temp'] is None or weather_info['temp'] > weather_aggregate[city]['max_temp']:
        weather_aggregate[city]['max_temp'] = weather_info['temp']

    if weather_aggregate[city]['min_temp'] is None or weather_info['temp'] < weather_aggregate[city]['min_temp']:
        weather_aggregate[city]['min_temp'] = weather_info['temp']

    # Track dominant weather condition
    condition = weather_info['main']
    if condition not in weather_aggregate[city]['dominant_conditions']:
        weather_aggregate[city]['dominant_conditions'][condition] = 0
    weather_aggregate[city]['dominant_conditions'][condition] += 1

alerts = []

def check_alert(city, weather_info):
    if weather_info['temp'] > 35:
        alerts.append(f"Alert for {city}: Temperature exceeded 35°C")
        send_email_alert(f"Temperature Alert for {city}", f"The temperature in {city} exceeded 35°C: {weather_info['temp']} °C")

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # Send to yourself or another recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

def plot_temperature(city):
    if city in weather_aggregate:
        temperatures = weather_aggregate[city]['temps']
        plt.figure(figsize=(10, 5))
        plt.plot(temperatures, marker='o', linestyle='-', color='b')
        plt.title(f'Temperature Trend in {city}')
        plt.xlabel('Update Number')
        plt.ylabel('Temperature (°C)')
        plt.xticks(range(len(temperatures)), [f'Update {i+1}' for i in range(len(temperatures))])
        plt.grid()
        plt.savefig(f'static/{city}_temperature_trend.png')  # Save the plot as an image
        plt.close()  # Close the plot to free up memory
    else:
        print(f"No data available for {city}")

app = Flask(__name__)

@app.route('/')
def index():
    init_db()  # Initialize the database
    weather_data = fetch_weather_for_cities()
    
    # Store aggregated data into the database
    for city in CITIES.keys():
        avg_temp = sum(weather_aggregate[city]['temps']) / len(weather_aggregate[city]['temps']) if weather_aggregate[city]['temps'] else 0
        max_temp = weather_aggregate[city]['max_temp']
        min_temp = weather_aggregate[city]['min_temp']
        humidity = weather_aggregate[city]['humidity'][-1] if weather_aggregate[city]['humidity'] else 0
        wind_speed = weather_aggregate[city]['wind_speed'][-1] if weather_aggregate[city]['wind_speed'] else 0
        store_weather_summary(city, datetime.now().date(), avg_temp, max_temp, min_temp, humidity, wind_speed)
        
        plot_temperature(city)
    
    return render_template('index.html', weather_data=weather_aggregate, alerts=alerts)

def store_weather_summary(city, date, avg_temp, max_temp, min_temp, humidity, wind_speed):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather_summary (city, date, avg_temp, max_temp, min_temp, humidity, wind_speed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (city, date, avg_temp, max_temp, min_temp, humidity, wind_speed))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
