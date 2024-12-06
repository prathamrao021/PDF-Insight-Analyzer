# from datetime import datetime, time, timezone
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import glob
from src.backend.process_data import fetchincidents, extractincidents, convert_data_to_numeric
from sklearn.cluster import DBSCAN
# import requests
import urllib.request
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'src/backend/uploads'
RESOURCE_FOLDER = 'src/backend/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)





@app.post("/upload_files")
async def upload_file(files: list[UploadFile] = File(...)):
    
    upload_file = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
    for f in upload_file:
        os.remove(f)

    resource_file = glob.glob(os.path.join(RESOURCE_FOLDER, '*'))
    for f in resource_file:
        os.remove(f)
    
    for file in files:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, 'wb') as file_object:
            file_object.write(await file.read())
    return JSONResponse(content={"message": "Files uploaded successfully"})





@app.post("/upload_urls")
async def upload_urls(urls: dict):
    print(urls)
    upload_file = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
    for f in upload_file:
        os.remove(f)

    resource_file = glob.glob(os.path.join(RESOURCE_FOLDER, '*'))
    for f in resource_file:
        os.remove(f)
    for url in urls['urls']:
        try:
            # delete all the files in the folder

            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            }
            filename = url.split('/')[-1]

            file_location = os.path.join(UPLOAD_FOLDER, filename)

            data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
            with open(file_location, 'wb') as file_object:
                file_object.write(data)
        except urllib.error.URLError as e:
            raise HTTPException(status_code=400, detail=f"Failed to download file from URL: {url}. Error: {str(e)}")
    return JSONResponse(content={"message": "URLs processed and files downloaded successfully"})





@app.get("/get_plot_data") 
async def get_plot_data():
    pdf_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*.pdf'))
    combined_data = pd.DataFrame()
    for pdf_file in pdf_files:
        incidents = fetchincidents(pdf_file)
        separated_data = extractincidents(incidents)
        encoded_data = convert_data_to_numeric(separated_data)
        combined_data = pd.concat([combined_data, pd.DataFrame(encoded_data)], ignore_index=True)

    kmeans = KMeans(n_clusters=5, random_state=42)
    combined_data['Cluster'] = kmeans.fit_predict(combined_data)

    # dbscan = DBSCAN(eps=0.5, min_samples=5)
    # combined_data['Cluster'] = dbscan.fit_predict(combined_data)

    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(combined_data.drop(columns=['Cluster']))
    pca_data = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_data['Cluster'] = combined_data['Cluster']

    pca1 = PCA(n_components=3)
    principal_components1 = pca1.fit_transform(combined_data.drop(columns=['Cluster']))
    pca_data1 = pd.DataFrame(data=principal_components1, columns=['PC1', 'PC2', 'PC3'])
    pca_data1['Cluster'] = combined_data['Cluster']

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

    plot_data3d = [
        {
            'x': pca_data1[pca_data1['Cluster'] == cluster]['PC1'],
            'y': pca_data1[pca_data1['Cluster'] == cluster]['PC2'],
            'z': pca_data1[pca_data1['Cluster'] == cluster]['PC3'],
            'mode': 'markers',
            'type': 'scatter',
            'name': f'Cluster {cluster}'
        }
        for cluster in pca_data1['Cluster'].unique()
    ]

    plot_layout = {
        'title': 'PCA of Features by Cluster',
        'xaxis': {'title': 'PC1'},
        'yaxis': {'title': 'PC2'}
    }

    cluster_counts = combined_data['Cluster'].value_counts().to_dict()


    return {'plotData': plot_data, 'plotLayout': plot_layout, 'clusterCounts': cluster_counts, 'plotData3d': plot_data3d}  

