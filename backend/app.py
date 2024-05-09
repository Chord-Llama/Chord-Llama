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

        # if music_file.filename.endswith('.mxl'):
        #     with zipfile.ZipFile(music_file, "r") as zip_ref:
        #         zip_ref.extractall(original_music_xml_file)
        # else:
        #     original_music_xml_file = music_file

        # part_list, system_message, prompt = file_cleaner.music_xml_to_inputs(original_music_xml_file)

        with open('system.yaml', 'r') as file:
            system_message = file.read()

        with open('prompt.yaml', 'r') as file:
            prompt = file.read()

        data = json.dumps({
            "model": "chord-full:latest",
            "system": system_message,
            "prompt": prompt
        })

        with open("test.json", "w") as json_file:
            json.dump(data, json_file)

        model_response = "" 

        s = requests.Session()
        r = s.post("http://localhost:11434/api/generate", data=data, stream=True)
        for index, stream_object in enumerate(r.iter_lines()):
            if stream_object:
                response_string = stream_object.decode('utf-8')
                response_json = json.loads(response_string)
                response_str = response_json['response']
                model_response += response_str

                print(response_json)

                if index > 1000:
                    break

        print(model_response)

        # final_tree = file_reverter.revert_file(part_list, system_message, model_response)

        # with tempfile.NamedTemporaryFile() as temp_file:
        #     final_tree.write(temp_file, encoding='utf-8', xml_declaration=True)
        #     file_reverter.prettify_xml(temp_file)
        #     file_reverter.add_docstring(temp_file, original_music_xml_file)

        #     return send_file(temp_file, as_attachment=True)

        return model_response

if __name__ == '__main__':
    app.run(debug=True)