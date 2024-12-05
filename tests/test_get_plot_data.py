
from main import upload_file, upload_urls, get_plot_data
import urllib.request
import requests

BASE_URL = 'http://localhost:8000'


def test_get_plot_data():
    response = requests.get(f"{BASE_URL}/get_plot_data")
    assert response.status_code == 200