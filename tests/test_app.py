import pytest
import responses
from app import app, kelvin_to_celsius, get_weather, check_alert


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask application."""
    app.config['TESTING'] = True  # Set the testing mode
    with app.test_client() as client:
        yield client  # Return the test client

def test_index(client):
    """Test the index route."""
    response = client.get('/')  # Make a GET request to the index route
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    assert b'Weather Monitoring Dashboard' in response.data  # Check for expected content in the response

def convert_to_celsius(kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return kelvin - 273.15

def test_temperature_conversion():
    """Test temperature conversion functionality."""
    assert convert_to_celsius(300) == pytest.approx(26.85, rel=1e-2)  # Check the conversion accuracy
    assert convert_to_celsius(273.15) == 0.0  # Check the freezing point

@responses.activate
def test_get_weather():
    """Test fetching weather data from the API."""
    # Mock the API response for a specific city (Delhi)
    responses.add(
        responses.GET,
        'http://api.openweathermap.org/data/2.5/weather?id=1273294&appid=c12283b7442a198cddfa077663c39f6f',
        json={
            'weather': [{'main': 'Clear'}],  # Add the weather condition here
            'main': {'temp': 300, 'feels_like': 310},  # Example response
            'dt': 1633072800  # Example timestamp
        },
        status=200,
    )

    # Fetch weather for Delhi (City ID: 1273294)
    weather = get_weather(1273294)
    
    # Check that the temperature matches
    assert weather['temp'] == kelvin_to_celsius(300)  # Verify temperature conversion
    assert weather['main'] == 'Clear'  # Verify weather condition
    assert weather['feels_like'] == kelvin_to_celsius(310)  # Verify feels like temperature


def check_alert(city, weather_info):
    """Check if an alert should be triggered based on temperature."""
    threshold_temp = 35
    if weather_info['temp'] > threshold_temp:
        return f"Alert for {city}: Temperature exceeded {threshold_temp}°C"
    return None

def test_check_alert():
    """Test alert conditions."""
    assert check_alert('Delhi', {'temp': 36}) == "Alert for Delhi: Temperature exceeded 35°C"
    assert check_alert('Delhi', {'temp': 34}) is None  # No alert

if __name__ == "__main__":
    pytest.main()  # Run the tests
