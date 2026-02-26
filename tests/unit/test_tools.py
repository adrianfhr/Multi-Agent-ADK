import pytest
from src.agents.tools.info_tools import get_weather, get_country_info, get_exchange_rate, get_joke

def test_get_weather_success(mocker):
    # Mock geocode
    mock_geo_resp = mocker.Mock()
    mock_geo_resp.json.return_value = {
        "results": [{"name": "Tokyo", "latitude": 35.6895, "longitude": 139.6917}]
    }
    # Mock weather
    mock_weather_resp = mocker.Mock()
    mock_weather_resp.json.return_value = {
        "current": {"temperature_2m": 15.5, "relative_humidity_2m": 60, "wind_speed_10m": 12.0}
    }
    
    # Needs side_effect to return different responses for different calls
    mock_get = mocker.patch("httpx.Client.get")
    mock_get.side_effect = [mock_geo_resp, mock_weather_resp]
    
    result = get_weather("Tokyo")
    assert result["status"] == "success"
    assert "Tokyo" in result["report"]
    assert "15.5°C" in result["report"]

def test_get_country_info_success(mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{
        "name": {"common": "Japan"},
        "capital": ["Tokyo"],
        "region": "Asia",
        "population": 125000000
    }]
    mocker.patch("httpx.Client.get", return_value=mock_resp)
    
    result = get_country_info("Japan")
    assert result["status"] == "success"
    assert "Japan" in result["report"]
    assert "Tokyo" in result["report"]

def test_get_exchange_rate_success(mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "result": "success",
        "rates": {"IDR": 15000}
    }
    mocker.patch("httpx.Client.get", return_value=mock_resp)
    
    result = get_exchange_rate("USD", "IDR")
    assert result["status"] == "success"
    assert "15000" in result["report"]

def test_get_joke_success(mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "setup": "Why did the chicken cross the road?",
        "punchline": "To get to the other side."
    }
    mocker.patch("httpx.Client.get", return_value=mock_resp)
    
    result = get_joke()
    assert result["status"] == "success"
    assert "Why did the chicken" in result["report"]
