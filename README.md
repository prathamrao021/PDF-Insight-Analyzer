# PDF Insight Analyzer
This project is a web application that allows users to upload PDF files or provide URLs to PDF files, processes the data, and visualizes the clustering results using various charts. The application is built using Next.js for the frontend and FastAPI for the backend.


## Features

- Upload PDF files or provide URLs to PDF files.
- Process the uploaded files or URLs to extract data.
- Visualize the clustering results using 2D and 3D scatter plots and bar charts.
- Customize the legend position and appearance in the charts.

## Technologies Used

- **Frontend:** Next.js, React, react-plotly.js, react-chartjs-2
- **Backend:** FastAPI, scikit-learn, pandas, requests
- **Other:** Plotly, Chart.js

## Installation

### Prerequisites

- Node.js and npm
- Python and pip

### Backend Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/prathamrao021/cis6930fa24-project3
   cd cis6930fa24-project3

2. **Install pipenv if you haven't already:**
    ```sh
    pip install pipenv

3. **Create a virtual environment and install dependencies:**
    ```sh
    pipenv install

4. **Activate the virtual enviornment:**
    ```sh
    python -m pipenv shell

5. **Run the FastAPI server:**
    ```sh
    pipenv run fastapi dev main.py

### Frontend Setup

1. **Navigate to the frontend directory:**
    ```sh
    cd src
    cd frontedn

2. **Install the required npm packages:**
    ```sh
    npm install

3. **Run the Next.js development server:**
    ```sh
    npm run dev

### Usage
1. Open your browser and navigate to `http://localhost:3000`.
2. Use the form to upload PDF files or provide URLs to PDF files.
3. Click the "Upload" button to process the files or URLs.
4. View the clustering visualizations in the charts.

## Functions
### Backend Functions
- **upload_file:** Handles file uploads and saves them to the uploads directory.
    ```python
    @app.post("/upload_files")
    async def upload_file(files: list[UploadFile] = File(...)):
        for file in files:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_location, 'wb') as file_object:
                file_object.write(await file.read())
        return JSONResponse(content={"message": "Files uploaded successfully"})

- **upload_urls:** Receives a list of URLs, downloads the files from the URLs, and saves them to the resources directory.
    ```python
    @app.post("/upload_urls")
    async def upload_urls(urls: Urls):
        for url in urls.urls:
            try:
                headers = {
                    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                }
                filename = url.split('/')[-1]
                file_location = os.path.join(RESOURCES_FOLDER, filename)

                data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
                with open(file_location, 'wb') as file_object:
                    file_object.write(data)
            except urllib.error.URLError as e:
                raise HTTPException(status_code=400, detail=f"Failed to download file from URL: {url}. Error: {str(e)}")
        return JSONResponse(content={"message": "URLs processed and files downloaded successfully"})

- **get_plot_data:** Processes the uploaded files or downloaded files, performs clustering, and returns the data for visualization.
    ```python
    @app.get("/get_plot_data")
    async def get_plot_data():
        pdf_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*.pdf'))
        combined_data = pd.DataFrame()
        for pdf_file in pdf_files:
            # Placeholder functions for extracting and processing data
            incidents = fetchincidents(pdf_file)
            separated_data = extractincidents(incidents)
            encoded_data = convert_data_to_numeric(separated_data)
            combined_data = pd.concat([combined_data, pd.DataFrame(encoded_data)], ignore_index=True)

        if combined_data.empty:
            return JSONResponse(content={"message": "No data available for plotting"}, status_code=204)

        # Use DBSCAN for clustering
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        combined_data['Cluster'] = dbscan.fit_predict(combined_data)

        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(combined_data.drop(columns=['Cluster']))
        pca_data = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
        pca_data['Cluster'] = combined_data['Cluster']

        plot_data = [
            {
                'x': pca_data[pca_data['Cluster'] == cluster]['PC1'],
                'y': pca_data[pca_data['Cluster'] == cluster]['PC2'],
                'mode': 'markers',
                'type': 'scatter',
                'name': f'Cluster {cluster}'
            }
            for cluster in pca_data['Cluster'].unique()
        ]

        plot_layout = {
            'title': 'PCA of Features by Cluster',
            'xaxis': {'title': 'PC1'},
            'yaxis': {'title': 'PC2'}
        }

        # Calculate cluster counts
        cluster_counts = combined_data['Cluster'].value_counts().to_dict()

        return {'`plotData': plot_data, 'plotLayout': plot_layout, 'clusterCounts': cluster_counts}

### Test Functions(For this the backend sever needs to be turned on)


- **test_upload_file:** Tests the /upload_files endpoint.
    ```python
    def test_upload_file():
        files = {'files': open('tests/testfile.pdf', 'rb')}
        response = requests.post(f"{BASE_URL}/upload_files", files=files)
        assert response.status_code == 200
        assert response.json()['message'] == 'Files uploaded successfully'

- **test_upload_urls:** Tests the /upload_urls endpoint.
    ```python
    def test_upload_urls():
        data = {
            "urls": ["http://example.com/testfile.pdf"]
        }
        response = requests.post(f"{BASE_URL}/upload_urls", json=data)
        assert response.status_code == 200
        assert response.json()['message'] == 'URLs processed and files downloaded successfully'

- **test_get_plot_data:** Tests the /get_plot_data endpoint.
    ```python
    def test_get_plot_data():
        response = requests.get(f"{BASE_URL}/get_plot_data")
        assert response.status_code == 200

## Demo Video (not the explained video)
[Link](https://github.com/user-attachments/assets/b15a1009-fd20-441e-a753-6650044a4596)

## Bugs and Assumptions
### Bugs
- File Upload Issues: There might be issues with uploading large PDF files due to size limitations.- URL Processing Errors: Some URLs might fail to download if the server is unreachable or if the URL is invalid.
- Data Extraction Errors: The data extraction process might fail for certain PDF formats that are not supported by the extraction logic.
- Clustering Accuracy: The clustering results might not be accurate if the data is not properly preprocessed or if the clustering parameters are not well-tuned.
- Unavailable Resources: The use of Geolocation API from Google has used all of my credits in testing and debugging and so, Geolocation API is not used on addresses.

### Assumptions
- PDF Format: It is assumed that the uploaded PDF files follow a specific format that the extraction logic can handle.
- Valid URLs: It is assumed that the provided URLs are valid and point to accessible PDF files.
- Data Quality: It is assumed that the data extracted from the PDF files is clean and suitable for clustering.
- Environment Setup: It is assumed that the environment is set up correctly with all the necessary dependencies installed.
