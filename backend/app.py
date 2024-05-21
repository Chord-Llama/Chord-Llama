import json
import os
import tempfile
import zipfile
from io import BytesIO
from xml.etree.ElementTree import Element, ElementTree

import requests
from flask import Flask, Response, jsonify, make_response, request, send_file

import file_cleaner

app = Flask(__name__)


@app.route("/generate-inputs", methods=["POST"])
def generate_inputs():
    files = request.files

    music_xml_file = files["music_xml_file"]

    if music_xml_file.filename.endswith(".mxl"):
        with zipfile.ZipFile(music_xml_file, "r") as zip_ref:
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_ref.extractall(tmpdir)
                file_path = os.path.join(tmpdir, "musicXML.xml")
                with open(file_path, "r") as f:
                    # Read the contents of the file
                    # original_music_xml_file = f.read()
                    # original_music_xml_file = '\n'.join(original_music_xml_file.splitlines()[2:])
                    part_list, system_message, prompt = (
                        file_cleaner.music_xml_to_inputs(f)
                    )

                    print(system_message)

                    return jsonify({"system_message": system_message, "prompt": prompt})

    original_music_xml_file = music_xml_file

    part_list, system_message, prompt = file_cleaner.music_xml_to_inputs(
        original_music_xml_file
    )

    return jsonify({"system_message": system_message, "prompt": prompt})


@app.route("/ollama-request", methods=["POST"])
def ollama_request():
    files = request.files

    system_file = files["system_file"]
    prompt_file = files["prompt_file"]

    system_message = system_file.read().decode("utf-8")
    prompt = prompt_file.read().decode("utf-8")

    data = json.dumps(
        {
            "model": "jaspann/llama-3-chord-llama:latest",
            "system": system_message,
            "prompt": prompt,
        }
    )

    print("sending data to Ollama...")

    s = requests.Session()
    r = s.post("http://localhost:11434/api/generate", data=data, stream=True)

    def generate():
        model_response = ""

        for index, stream_object in enumerate(r.iter_lines()):
            if stream_object:
                response_string = stream_object.decode("utf-8")
                response_json = json.loads(response_string)
                response_str = response_json["response"]

                yield response_json["response"]

                model_response += response_str

                print(response_json)

                if index > 500:
                    print(f"index: {index}")
                    break

        print(model_response)

    return Response(generate(), mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
