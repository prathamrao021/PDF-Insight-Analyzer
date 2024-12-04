'use client';

import { title } from "@/components/primitives";
import { Navbar1 } from "@/components/navbar1";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import { useRef, useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { Oval } from 'react-loader-spinner';
import { Bar } from 'react-chartjs-2';

// Dynamically import react-plotly.js
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function UploadPage() {
  const uploadFormRef = useRef<HTMLFormElement>(null);
  const [plotData, setPlotData] = useState<any[]>([]);
  const [plotData3d, setPlotData3d] = useState<any[]>([]);
  const [clusterCounts, setClusterCounts] = useState<any>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [showCharts, setShowCharts] = useState<boolean>(false);
  const [urls, setUrls] = useState<string[]>(['']); // State to manage list of URLs

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFormRef.current) return;
  
    const formData = new FormData(uploadFormRef.current);
    const files = formData.getAll('files') as File[];
  
    const validUrls = urls.filter((url) => url.trim() !== '');
    console.log('validUrls:', validUrls);
    console.log('files:', files[0]['name'].length === 0);
    
    if (files[0]['name'].length > 0 && validUrls.length > 0) {
      window.alert('Please provide either files or URLs, not both');
      console.error('Please provide either files or URLs, not both');
      setLoading(false);
      return;
    }
  
    // If neither files nor URLs are provided
    if (files[0]['name'].length === 0 && validUrls.length === 0) {
      window.alert('Please provide a file or a URL');
      console.error('Please provide a file or a URL');
      setLoading(false);
      return;
    }
  
    try {
      setLoading(true);
      setShowCharts(true);
  
      // Handle file uploads
      if (files[0]['name'].length > 0) {
        const fileFormData = new FormData();
        files.forEach((file) => fileFormData.append('files', file));
  
        const fileResponse = await fetch('http://localhost:8000/upload_files', {
          method: 'POST',
          body: fileFormData,
        });
  
        if (!fileResponse.ok) {
          console.error('File upload failed');
          setLoading(false);
          return;
        }
      }
  
      // Handle URL submissions
      if (validUrls.length > 0) {
        const urlResponse = await fetch('http://localhost:8000/upload_urls', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ urls: validUrls }),
        });
  
        if (!urlResponse.ok) {
          console.error('URL processing failed');
          setLoading(false);
          return;
        }
      }
  
      // Fetch plot data after successful uploads
      await fetchPlotData();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };
  

  const fetchPlotData = async () => {
    try {
      const response = await fetch('http://localhost:8000/get_plot_data');
      const data = await response.json();
      console.log('Plot data:', data);
      setPlotData(data.plotData);
      // setPlotLayout(data.plotLayout);
      setClusterCounts(data.clusterCounts);
      setPlotData3d(data.plotData3d);
    } catch (error) {
      console.error('Error fetching plot data:', error);
    } finally {
      setLoading(false);
    }
  };

  const addUrlInput = () => {
    setUrls([...urls, '']);
  };

  const handleUrlChange = (index: number, value: string) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const handleUrlDelete = (index: number) => {
    if (urls.length > 1) {
      const newUrls = urls.filter((_, i) => i !== index);
      setUrls(newUrls);
    }
  };

  return (
    <>
      <Navbar1 />
      <div className="p-20">
        <form className="upload" ref={uploadFormRef} onSubmit={handleUpload}>
          <Input
            className="mb-4"
            radius="full"
            type="file"
            accept=".pdf"
            name="files"
            multiple
          />
          <h1 className="text-xl ml-20 mb-4">OR</h1>
          {urls.map((url, index) => (
            <div key={index} className="mb-4 flex items-center">
              <Input
                radius="full"
                type="text"
                placeholder="Enter URL"
                value={url}
                onChange={(e) => handleUrlChange(index, e.target.value)}
                className="flex-grow"
              />
              {urls.length > 1 && (
                <Button type="button" color="danger" onClick={() => handleUrlDelete(index)} className="ml-2">
                  Delete
                </Button>
              )}
            </div>
          ))}
         
          <Button type="submit" color="success">
            Upload
          </Button>
          <Button className="ml-3" type="button" color="primary" onClick={addUrlInput}>
            Add URL
          </Button>
        </form>
      </div>

      <div className={`pl-20 pr-20 ${showCharts ? '' : 'hidden'}`}>
        <h1 className="text-3xl flex justify-center items-center font-bold mb-4">Charts</h1>
        {loading ? (
          <div className="flex justify-center items-center">
            <Oval
              height={80}
              width={80}
              color="#4fa94d"
              visible={true}
              ariaLabel="oval-loading"
              secondaryColor="#4fa94d"
              strokeWidth={2}
              strokeWidthSecondary={2}
            />
          </div>
        ) : (
          <>
          <div className="p-10 flex justify-center items-center">
          <Plot
            data={plotData.map((cluster) => ({
              x: Object.values(cluster.x),
              y: Object.values(cluster.y),
              mode: cluster.mode,
              type: 'scatter',
              name: cluster.name,
              marker: {
                colors: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  'rgba(153, 102, 255, 0.6)',
                ],
              },
            }))}
            layout={{
              title: "Clustering Visualization",
              xaxis: { title: "PC1" },
              yaxis: { title: "PC2" },
              legend: {
                x: 1, // Position the legend to the right
                y: 0, // Position the legend at the bottom
                orientation: 'v', // Vertical orientation
                font: {
                  family: 'Arial, sans-serif',
                  size: 12,
                  color: '#000',
                },
                bgcolor: '#E2E2E2',
                bordercolor: '#FFFFFF',
                borderwidth: 2,
              },
            }}
            style={{ width: 'auto', height: 'auto' }}
          />
          </div>
          <div className="p-10 flex justify-center items-center">
          <Plot
            data={plotData3d.map((cluster) => ({
              x: Object.values(cluster.x),
              y: Object.values(cluster.y),
              z: Object.values(cluster.z),
              mode: cluster.mode,
              type: 'scatter3d',
              name: cluster.name,
              marker: {
                colors: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  'rgba(153, 102, 255, 0.6)',
                ],
              },
            }))}
            layout={{
              title: "Clustering Visualization",
              xaxis: { title: "PC1" },
              yaxis: { title: "PC2" },
              zaxis: { title: "PC3" },
              legend: {
                x: 1, // Position the legend to the right
                y: 0, // Position the legend at the bottom
                orientation: 'v', // Vertical orientation
                font: {
                  family: 'Arial, sans-serif',
                  size: 12,
                  color: '#000',
                },
                bgcolor: '#E2E2E2',
                bordercolor: '#FFFFFF',
                borderwidth: 2,
              },
            }}
            style={{ width: 'auto', height: 'auto' }}
          />
          </div>
          <div className="p-10 flex justify-center items-center">
            <Plot
              data={[
                {
                  x: Object.keys(clusterCounts).map((key) => `Cluster ${key}`), // X-axis labels
                  y: Object.values(clusterCounts), // Y-axis values
                  type: 'bar', // Bar chart type
                  marker: {
                    color: [
                      'rgba(255, 99, 132, 0.6)',
                      'rgba(54, 162, 235, 0.6)',
                      'rgba(255, 206, 86, 0.6)',
                      'rgba(75, 192, 192, 0.6)',
                      'rgba(153, 102, 255, 0.6)',
                    ],
                  },
                },
              ]}
              layout={{
                title: 'Cluster Counts',
                xaxis: {
                  title: 'Clusters',
                },
                yaxis: {
                  title: 'Counts',
                },
                showlegend: false,
              }}
              style={{ width: 'auto', height: 'auto' }}
            />
          </div>
          <div className="p-10 flex justify-center items-center">
            <Plot
              data={[
                {
                  labels: Object.keys(clusterCounts).map((key) => `Cluster ${key}`), // Cluster labels
                  values: Object.values(clusterCounts), // Corresponding counts
                  type: 'pie', // Chart type
                  hole: 0.4, // Use this to make it a donut chart (optional)
                  marker: {
                    colors: [
                      'rgba(255, 99, 132, 0.6)',
                      'rgba(54, 162, 235, 0.6)',
                      'rgba(255, 206, 86, 0.6)',
                      'rgba(75, 192, 192, 0.6)',
                      'rgba(153, 102, 255, 0.6)',
                    ],
                  },
                },
              ]}
              layout={{
                title: 'Cluster Distribution',
                legend: {
                  x: 1, // Position the legend to the right
                  y: 0, // Position the legend at the bottom
                  orientation: 'v', // Vertical orientation
                  font: {
                    family: 'Arial, sans-serif',
                    size: 12,
                    color: '#000',
                  },
                  bgcolor: '#E2E2E2',
                  bordercolor: '#FFFFFF',
                  borderwidth: 2,
                },
              }}
              style={{ width: 'auto', height: 'auto' }}
            />
          </div>
          </>
        )}
      </div>
    </>
  );
}