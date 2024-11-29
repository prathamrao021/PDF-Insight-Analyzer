'use client';
import { title } from "@/components/primitives";
import { Navbar1 } from "@/components/navbar1";
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import { useRef } from 'react';

export default function UploadPage() {
  const uploadFormRef = useRef<HTMLFormElement>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFormRef.current) return;

    const formData = new FormData(uploadFormRef.current);
    const files = formData.getAll('files') as File[];

    for (const file of files) {
      if (file.type !== 'application/pdf') {
        console.error('Only PDF files are allowed');
        return;
      }
    }

    try {
      const response = await fetch('http://localhost:8000/upload_files', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        console.log('Files uploaded successfully');
        window.location.reload();
        // popup to confirm that submission is done
      } else {
        console.error('File upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <>
      <Navbar1 />
      <div className="p-20">
        <form className="upload" ref={uploadFormRef} onSubmit={handleUpload}>
          <Input className="mb-4" radius="full" type="file" accept=".pdf" name="files" multiple required />
          <Button type="submit" color="success">Upload</Button>
        </form>
      </div>
    </>
  );
}