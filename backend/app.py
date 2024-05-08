from flask import Flask, jsonify, request, Response, send_file
import json
import requests
from xml.etree.ElementTree import Element, ElementTree
import tempfile

import file_cleaner
import file_reverter

app = Flask(__name__)




@app.route('/ollama-request', methods=['POST'])
def ollama_request():
    files = request.files

    music_file = files['music_file']

    if music_file.filename.endswith('.mxl'):
        raw_file_contents: str = file_cleaner.unzip_file(music_file)
    else:
        raw_file_contents: str = music_file.read()

    part_list, system_message, prompt = file_cleaner.music_xml_to_inputs(raw_file_contents)

    data = json.dumps({
        "model": "llama-3-chord-llama-1:latest",
        "system": system_message,
        "prompt": prompt
    })

    model_response = "" 

    s = requests.Session()
    r = s.post("http://localhost:11434/api/generate", data=data, stream=True)
    for stream_object in r.iter_lines():
        if stream_object:
            model_response += stream_object['response']

    final_tree = file_reverter.revert_file(part_list, system_message, model_response)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        final_tree.write(temp_file, encoding='utf-8', xml_declaration=True)
        file_reverter.prettify_xml(temp_file)
        file_reverter.add_docstring(temp_file, raw_file_contents)

        return send_file(temp_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)