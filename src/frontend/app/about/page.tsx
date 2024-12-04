'use client';
import { subtitle, title } from "@/components/primitives";
import { Navbar1 } from "@/components/navbar1"; 
export default function AboutPage() {
  const features = [
    "Data Input: Users can upload Norman Police Department incident PDFs or provide URLs to these documents.",
    "Multiple Visualizations: We offer three distinct ways to view and analyze the data:",
    "Interactive Interface: Our user-friendly design allows for easy navigation and data exploration."
  ];

  const visualizations = [
    "Clustering of records to identify patterns and groupings",
    "Bar graph comparisons for easy statistical analysis",
    "A unique third visualization (specify the type you've chosen)"
  ];
  return (
    <>
    <Navbar1/>
    <div className="p-20">
        <h1 className="text-3xl font-bold mb-4">About</h1>
        <p className="mb-4">Welcome to our Norman Police Department Incident Data Visualization Tool.</p>
        
        <h1 className="text-3xl font-bold mb-4">Purpose</h1>
        <p className="mb-4">This interactive web interface is designed to provide insightful visualizations of incident data from the Norman Police Department. Our goal is to make this information more accessible and understandable to the public, researchers, and policymakers.</p>
        
        <h1 className="text-3xl font-bold mb-4">Features</h1>
        <ol className="list-decimal pl-5 mb-4">
          {features.map((feature, index) => (
            <li key={index} className="mb-2">{feature}</li>
          ))}
        </ol>
        <ul className="list-disc pl-10 mb-4">
          {visualizations.map((vis, index) => (
            <li key={index} className="mb-1">{vis}</li>
          ))}
        </ul>
        <h1 className="text-3xl font-bold mb-4">How It Works</h1>
        <p className="mb-4">Our tool follows a simple three-step process:</p>
        <ol className="list-decimal pl-5 mb-4">
          <li>Upload your PDF or provide a URL to the Norman PD incident report.</li>
          <li>Our system processes the data using advanced algorithms.</li>
          <li>View the generated visualizations to gain insights into the incident data.</li>
        </ol>
        <h1 className="text-3xl font-bold mb-4">Project Background</h1>
        <p className="mb-4">This tool was developed as part of a semester-long project focusing on different aspects of the data pipeline. It represents the culmination of skills acquired in data collection, processing, and visualization.</p>
        <h1 className="text-3xl font-bold mb-4">Why It Matters</h1>
        <p className="mb-4">By providing easy-to-understand visualizations of police incident data, we aim to:</p>
        <ul className="list-disc pl-10 mb-4">
          <li>Increase transparency in local law enforcement activities</li>
          <li>Aid in community awareness and safety initiatives</li>
          <li>Provide valuable tools for researchers and policymakers</li>
        </ul>
        <h1 className="text-3xl font-bold mb-4">About the Developers</h1>
        <p className="mb-4">This project was created by Pratham Rao. We are passionate about using data science to make a positive impact in our community.</p>
        <h1 className="text-3xl font-bold mb-4">Feedback and Contact</h1>
        <p className="mb-4">We welcome your feedback and suggestions. Please contact us at  with any questions or comments.</p>
        <a className="text-red-400" href="mailto:prathamrao021@gmail.com">Click here to mail me.</a>
      </div>
    
    </>
  );
}
