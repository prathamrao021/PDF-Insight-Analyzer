from main import upload_file, upload_urls, get_plot_data
import urllib.request
import requests

BASE_URL = 'http://localhost:8000'

def test_upload_url():
    data = {
        "urls": ["https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-01_daily_incident_summary.pdf"]
    }
    response = requests.post(f"{BASE_URL}/upload_urls", json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'URLs processed and files downloaded successfully'

