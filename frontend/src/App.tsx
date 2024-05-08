import React, { ChangeEvent, useState } from 'react';

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prompt, setPrompt] = useState<string>('');

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('music_file', selectedFile);
      // formData.append('prompt', prompt)
      
      // Example fetch request
      fetch('/ollama-request', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        // Handle response
      })
      .catch(error => {
        // Handle error
      });
    }
  };

  const handlePromptChange = (event: ChangeEvent<HTMLInputElement>) => {
    setPrompt(event.target.value); // Update prompt state when text box value changes
  };

  // accept=".xml,.mxl,.musicxml"

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <input type="text" value={prompt} onChange={handlePromptChange} placeholder="Enter prompt" />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUpload;
