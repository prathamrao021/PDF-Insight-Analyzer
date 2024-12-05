from main import upload_file, upload_urls, get_plot_data
import urllib.request
import requests

BASE_URL = 'http://localhost:8000'

def test_upload_file():
    files = {'files': open('tests/testfile.pdf', 'rb')}
    response = requests.post(f"{BASE_URL}/upload_files", files=files)
    assert response.status_code == 200
    assert response.json()['message'] == 'Files uploaded successfully'

