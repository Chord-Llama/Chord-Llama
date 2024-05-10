import React, { ChangeEvent, useState, useEffect } from 'react';

const FileUpload: React.FC = () => {
  const [systemFile, setSystemFile] = useState<File | null>(null);
  const [promptFile, setPromptFile] = useState<File | null>(null);
  
  useEffect(() => {
    document.title = "Chord Llama";
  }, []);

  const handleSystemFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSystemFile(file);
    }
  };

  const handlePromptFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setPromptFile(file);
    }
  };

  const handleUpload = () => {
    if (systemFile && promptFile) {
      const formData = new FormData();
      formData.append('system_file', systemFile);
      formData.append('prompt_file', promptFile);
      
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

  return (
    <div>
      <div style={{ marginBottom: '10px', paddingLeft: '10px' }}>
      <text>Upload attributes file:  </text>
      <input type="file" onChange={handleSystemFileChange} />
      </div>
      <div style={{ marginBottom: '10px', paddingLeft: '10px' }}>
      <text>Upload measures file: </text>
      <input type="file" onChange={handlePromptFileChange} />
      </div>
      <button onClick={handleUpload} style={{marginLeft: '10px'}}>Upload</button>
    </div>
  );
};

export default FileUpload;
