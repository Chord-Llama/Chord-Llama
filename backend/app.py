from flask import Flask, jsonify, request, Response, send_file
import json
import requests
from xml.etree.ElementTree import Element, ElementTree
import tempfile
import zipfile

import file_cleaner
import file_reverter

app = Flask(__name__)




@app.route('/ollama-request', methods=['POST'])
def ollama_request():
    files = request.files

    music_file = files['music_file']

    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as original_music_xml_file:

        if music_file.filename.endswith('.mxl'):
            with zipfile.ZipFile(music_file, "r") as zip_ref:
                zip_ref.extractall(original_music_xml_file)
        else:
            original_music_xml_file = music_file

        part_list, system_message, prompt = file_cleaner.music_xml_to_inputs(original_music_xml_file)

        # print(prompt)

        data = json.dumps({
            "model": "jaspann/llama-3-chord-llama-2:latest",
            "system": system_message,
            "prompt": prompt
        })

        with open("test.json", "w") as json_file:
            json.dump(data, json_file)

        model_response = "" 

        s = requests.Session()
        r = s.post("http://localhost:11434/api/generate", data=data, stream=True)
        for stream_object in r.iter_lines():
            if stream_object:
                print(stream_object)
                response_str = stream_object['response'].decode('utf-8')
                model_response += response_str

        final_tree = file_reverter.revert_file(part_list, system_message, model_response)

        with tempfile.NamedTemporaryFile() as temp_file:
            final_tree.write(temp_file, encoding='utf-8', xml_declaration=True)
            file_reverter.prettify_xml(temp_file)
            file_reverter.add_docstring(temp_file, original_music_xml_file)

            return send_file(temp_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)