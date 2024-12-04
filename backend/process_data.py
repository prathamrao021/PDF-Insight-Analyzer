from pypdf import PdfReader
import pandas as pd
import os
import glob
import requests
import time
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


API_KEY = "..."

def fetchincidents(pdf):
    reader = PdfReader(pdf)
    data = ''
    for page in reader.pages:
        data = data + "\n" + page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)

    return data


def extractincidents(data):

    lines = (data.split("\n"))[4:-1]
    rows = []

    temp_row = []
    temp_text = ""
    for line in lines:
        split_line = [field.strip() for field in line.split("          ") if field.strip()]

        if len(split_line) < 5:
            if len(temp_row) > 0:
                temp_row[2] += " " + split_line[0]
                
        else:
            if len(temp_row) == 5:
                temp_text += "\t".join(temp_row)
                temp_text += "\n"
                rows.append(temp_row)
            temp_row = split_line 

    if len(temp_row) == 5:
        rows.append(temp_row)
        temp_text += "\t".join(temp_row)


    with open('resources/data.tsv','a') as file:
        file.write(temp_text)
    
    return rows

def get_lat_lng(address):
    time.sleep(0.1)
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": API_KEY}
    response = requests.get(base_url, params=params).json()
    # print(response)
    if response['status'] == "OK":
        location = response['results'][0]['geometry']['location']

        # print(location['lat'], location['lng'])

        return location['lat'], location['lng']
    else:
        print('0, 0')
        return 0, 0

def convert_data_to_numeric(data):
    data = pd.DataFrame(data, columns=["Date/Time", "IncidentNumber", "Location", "Nature", "IncidentOri"])
    
    # try:
    #     data['Latitude'], data['Longitude'] = zip(*data['Location'].apply(get_lat_lng))
    # except:
    #     data['Latitude'], data['Longitude'] = 0, 0

    data['Hour'] = pd.to_datetime(data['Date/Time']).dt.hour
    data['Day'] = pd.to_datetime(data['Date/Time']).dt.day
    
    # missing_locations = data[data[['Latitude', 'Longitude']].isna().any(axis=1)]

    encoder = LabelEncoder()
    data['NatureEncoded'] = encoder.fit_transform(data['Nature'])
    data['Day'] = encoder.fit_transform(data['Day'])

    data = data.drop(columns=['Date/Time', 'Location', 'Nature', 'IncidentNumber', 'IncidentOri'])

    # print(data)

    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    return data

def write_processded_data(data):
    data.to_csv('resources/processed_data.csv', index=False)

def pca_conversion(data):
    pca = PCA(n_components=2)  # Reduce to 2 components for visualization
    principal_components = pca.fit_transform(data.drop(columns=['Cluster']))
    pca_data = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_data['Cluster'] = data['Cluster']
    return pca_data


#how the workflow will look like
def main_workflow():
    pdf_files = glob.glob(os.path.join('uploads', '*.pdf'))

    combined_data = pd.DataFrame()
    # clusters = pd.DataFrame()
    for pdf_file in pdf_files:
        incidents = fetchincidents(pdf_file)
        separated_data = extractincidents(incidents)
        encoded_data = convert_data_to_numeric(separated_data)
        combined_data = pd.concat([combined_data, pd.DataFrame(encoded_data)], ignore_index=True)

    kmeans = KMeans(n_clusters=5, random_state=42)
    combined_data['Cluster'] = kmeans.fit_predict(combined_data)

    
    write_processded_data(combined_data)

    combined_linear_data = pca_conversion(combined_data)


# if __name__ == "__main__":
#     main_workflow()
