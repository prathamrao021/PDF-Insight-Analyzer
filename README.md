# cis6930fa24-project3
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
## Video
[Link](https://github.com/user-attachments/assets/b15a1009-fd20-441e-a753-6650044a4596)
## Bugs and Assumptions

## to-do
- [ ] readme
- [ ] video
- [ ] COLLABORATORS
