# Chord Llama: Generating sheet music using Llama

This is the application to run the Chord Llama Model. From a MusicXML file, it tries to continue the music. The model requires Ollama to be installed.

## Model
This application uses a fine tuned version of Llama 3.
- HuggingFace model: https://huggingface.co/datasets/Chord-Llama/chord_llama_data_mini_train
- Ollama Model: https://ollama.com/jaspann/llama-3-chord-llama
- Dataset: https://huggingface.co/datasets/Chord-Llama/chord_llama_data_mini_train/tree/main
- Dataset Script: https://huggingface.co/datasets/Chord-Llama/chord_llama_dataset/blob/main/music_xml_converter.ipynb
- Training / Testing Script: https://huggingface.co/Chord-Llama/Llama-3-chord-llama-fullModel/blob/main/Selection_Training.ipynb

## Installation
We could not get Docker working with the project, so installation needs to be done manually for now.

### Frontend
- `cd frontend` to go to the frontend directory
- `npm run build` to set up the frontend
- `npm run start` to start up the app

### Backend
- `cd backend` to go to the backend directory
- `python3 -m venv venv` to create a virtual environment
- `source venv/bin/activate` to activate the virtual environment
- `pip install -r requirements.txt` to install the required packages
- `flask run` to start the backend

### Ollama
- Follow the instructions to install [Ollama](https://ollama.com/)
- `ollama pull jaspann/llama-3-chord-llama` Pull the latest version of the model from the Ollama repository
