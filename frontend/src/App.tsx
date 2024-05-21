import React, { ChangeEvent, useState, useEffect } from 'react';

const FileUpload: React.FC = () => {
  // State to store the files
  const [systemFile, setSystemFile] = useState<File | null>(null);
  const [promptFile, setPromptFile] = useState<File | null>(null);
  const [musicXmlFile, setMusicXmlFile] = useState<File | null>(null);

  // State to store the text responces
  const [systemText, setSystemText] = useState('');
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  
  useEffect(() => {
    document.title = "Chord Llama";
  }, []);

  const handleSystemFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setSystemFile(file);
  
      const reader = new FileReader();
      reader.onload = (event) => {
        const fileContent = (event.target?.result as string) ?? '';
        
        setSystemText(fileContent);
      };
      reader.readAsText(file);
    }
  };

  const handlePromptFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setPromptFile(file);
  
      const reader = new FileReader();
      reader.onload = (event) => {
        const fileContent = (event.target?.result as string) ?? '';
        
        setInputText(fileContent);
      };
      reader.readAsText(file);
    }
  };

  const handleMusicXmlFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setMusicXmlFile(file);
    }
  };

  const convertFile = () => {
    if (musicXmlFile) {
      const formData = new FormData();
      formData.append('music_xml_file', musicXmlFile);

      fetch('/generate-inputs', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setSystemText(data['system_message']);
        setInputText(data['prompt']);
      })
      .catch(error => {
        setInputText('Error uploading file');
      });
    }
  }

  const handleUpload = () => {
    if ((systemText !== '' && inputText !== '')) {
      const formData = new FormData();
      
      const system_file_blob = new Blob([systemText], { type: "text/plain" });
      const system_file = new File([system_file_blob], "system_file.yaml");
      
      const prompt_file_blob = new Blob([inputText], { type: "text/plain" });
      const prompt_file = new File([prompt_file_blob], "prompt_file.yaml");

      formData.append('system_file', system_file);
      formData.append('prompt_file', prompt_file);
      
      // Example fetch request
      fetch('/ollama-request', {
        method: 'POST',
        body: formData
      })
      .then(response => response.text())
      .then(text => {
        setOutputText(text)
      })
      .catch(error => {
        // Handle error
      });
    }
  };

  return (
<div>
  <div style={{ marginRight: '10px', marginLeft: '10px' }}>
  <h1 >Chord Llama</h1>
  <p>Upload a MusicXML file or an attribute and measure YAML file to generate chord progressions</p>
  <p>Upload MusicXML file: </p>
  <input type="file" onChange={handleMusicXmlFileChange} />
  <button onClick={convertFile} style={{ marginRight: '10px' , marginLeft: '10px' }}>Convert MusicXML</button>
  <button onClick={handleUpload} style={{ marginRight: '10px', marginLeft: '10px' }}>Run Inference</button>
  </div>
  <div style={{ display: 'flex', flexWrap: 'wrap' }}>
    <div style={{ flex: 1, margin: '10px' }}>
      <h3>Attributes</h3>
      <div style={{ border: '1px solid #ccc', padding: '10px' }}>
        <p>Upload attributes file:  </p>
        <input type="file" onChange={handleSystemFileChange} />
        <pre style={{ border: '1px solid #ccc', padding: '10px' }}>{systemText}</pre>
      </div>
    </div>
    <div style={{ flex: 1, margin: '10px' }}>
      <h3>Measures</h3>
      <div style={{ border: '1px solid #ccc', padding: '10px' }}>
        <p>Upload measures file: </p>
        <input type="file" onChange={handlePromptFileChange} />
        <pre style={{ border: '1px solid #ccc', padding: '10px' }}>{inputText}</pre>
      </div>
    </div>
    <div style={{ flex: 1, margin: '10px' }}>
      <h3>Output</h3>
      <div style={{ border: '1px solid #ccc', padding: '10px' }}>
        <p>YAML Output: </p>
        <pre style={{ border: '1px solid #ccc', padding: '10px' }}>{outputText}</pre>
      </div>
    </div>
  </div>
</div>
  );
};

export default FileUpload;
