# Real-Time Weather Monitoring System

## Overview
This project implements a real-time data processing system for monitoring weather conditions using the OpenWeatherMap API. The system retrieves weather data for several major cities in India, processes this data to provide daily summaries, and alerts users when certain thresholds are exceeded.

## Features
- **Real-time Data Retrieval**: Continuously fetches weather data from OpenWeatherMap at configurable intervals.
- **Data Processing**: Converts temperature data from Kelvin to Celsius and calculates daily aggregates:
  - Average Temperature
  - Maximum Temperature
  - Minimum Temperature
  - Dominant Weather Condition
- **Alerting System**: Notifies users if certain temperature thresholds are exceeded.
- **Data Visualization**: Displays weather trends through graphical representations.
- **Persistent Storage**: Stores weather summaries in an SQLite database for historical analysis.

## Design Choices
- **Microservices Architecture**: The application is designed using a microservices approach where data retrieval, processing, and visualization are handled independently.
- **Database Choice**: SQLite is chosen for its simplicity and ease of use in small applications. It allows for persistent data storage without the need for a dedicated database server.
- **Data Visualization**: Matplotlib is used for visualizing temperature trends, making it easier to identify patterns over time.

## Dependencies
To run this application, ensure you have the following dependencies installed:
- **Python 3.x**
- **Flask**: Web framework for creating the application.
- **Requests**: For making HTTP requests to the OpenWeatherMap API.
- **Matplotlib**: For generating temperature trend graphs.
- **APScheduler**: For scheduling periodic weather data fetching.
- **SQLite**: For persistent data storage.

### Docker Setup
This application can also be run inside a Docker container. Below are the steps to set it up using Docker:

1. **Dockerfile**: Create a `Dockerfile` in the project root with the following content:

   ```Dockerfile
   # Use the official Python image from Docker Hub
   FROM python:3.9-slim

   # Set the working directory in the container
   WORKDIR /app

   # Copy the requirements file into the container
   COPY requirements.txt .

   # Install dependencies
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy the rest of the application code into the container
   COPY . .

   # Command to run the application
   CMD ["python", "app.py"]
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t weather-monitoring-app .
   ```

3. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 weather-monitoring-app
   ```

4. **Access the application**: Open a web browser and go to `http://127.0.0.1:5000` to view the dashboard.

## Installation Without Docker
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `config.py` file** with your OpenWeatherMap API key and city IDs:
   ```python
   API_KEY = 'your_api_key_here'
   CITIES = {
       'Delhi': '2988507',
       'Mumbai': '1275339',
       'Chennai': '1264527',
       'Bangalore': '1277333',
       'Kolkata': '1264520',
       'Hyderabad': '1264527'
   }
   ```

## Usage
1. **Start the Flask application**:
   ```bash
   python app.py
   ```
2. **Open a web browser** and go to `http://127.0.0.1:5000` to view the dashboard.

## Database
The project uses SQLite for persistent data storage. The database file `weather_data.db` will be created in the project directory. You can view the data using:
- SQLite command line interface
- [DB Browser for SQLite](https://sqlitebrowser.org/)

## Testing
To ensure the functionality of the system, unit tests can be run. The testing can cover the following areas:
1. **System Setup**: Verify the application starts correctly and connects to the OpenWeatherMap API using a valid API key.
2. **Data Retrieval**: Simulate API calls at configurable intervals and ensure the system retrieves weather data for specified locations correctly.
3. **Temperature Conversion**: Test the conversion of temperature values from Kelvin to Celsius (or Fahrenheit) based on user preference.
4. **Daily Weather Summary**: Simulate a sequence of weather updates and verify that daily summaries are calculated correctly, including average, maximum, and minimum temperatures and dominant weather condition.
5. **Alerting Thresholds**: Define user-configurable thresholds for temperature or weather conditions and verify that alerts are triggered only when a threshold is violated.

### Running Tests
You can create a separate test file, e.g., `test_app.py`, and run it using:
```bash
python -m unittest test_app.py
```

## Future Improvements
- Implement additional features for better data analysis.
- Support for real-time weather forecasts.
- Enhanced user interface with more detailed visualizations.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [OpenWeatherMap API](https://openweathermap.org/) for weather data.
- [Flask](https://flask.palletsprojects.com/) for web application framework.
- [Matplotlib](https://matplotlib.org/) for data visualization.
