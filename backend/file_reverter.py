
import lxml.etree as ET
from lxml import etree
from xml.etree.ElementTree import Element, ElementTree
import tempfile
import os
import yaml
import xmltodict
from io import StringIO


# encoding declaration is not supported for converting back. xmltodict.unparse() will automatically add the encoding declaration, so we need to remove it.
def remove_encoding_declaration(text: str) -> str:
    # Split the text into lines
    lines = text.splitlines()
    # Remove the first line and join the remaining lines back together
    return '\n'.join(lines[1:])

def prettify_xml(file):
    tree = ET.parse(file)
    ET.indent(tree)
    tree.write(file, encoding='utf-8', xml_declaration=True)

def add_docstring(file: str, original_song: str) -> None:
    
    file_contents = original_song.split("\n")
    docstring = file_contents[1]

    with open(file, 'r') as f:
        # Read the contents of the file
        file_contents = f.read()
        # add a docstring to the second line
        file_contents = file_contents.split("\n")
        file_contents.insert(1, docstring)
        file_contents = '\n'.join(file_contents)
        # Write the contents of the file
    with open(file, 'w') as f:
        f.write(file_contents)

def to_dict(yaml_text: str) -> dict:
    text_dict = yaml.safe_load(yaml_text)
    text_dict = {str(f"a{index:02d}_measure") : value for index, value in enumerate(text_dict)}
    text_dict = {"part" : text_dict}
    return text_dict

def revert_file(part_list: Element, system_message: str, model_response: str) -> ElementTree:

    instruction_yaml = to_dict(system_message)
    output_yaml = to_dict(model_response)

    # Convert the dictionary to XML
    parser = etree.XMLParser(recover=True, encoding='utf-8')

    instruction_xml = remove_encoding_declaration(xmltodict.unparse(instruction_yaml))
    instruction_tree: ElementTree = ET.parse(StringIO(instruction_xml), parser)

    output_xml = remove_encoding_declaration(xmltodict.unparse(output_yaml))
    output_tree: ElementTree = ET.parse(StringIO(output_xml), parser)

    instruction: Element = instruction_tree.getroot()
    output: Element = output_tree.getroot()

    for measure in instruction:
        measure.tag = measure.tag.split("_")[1]
        for element in measure:
            element.tag = element.tag.split("_")[1]
            
    for measure in output:
        measure.tag = measure.tag.split("_")[1]
        for element in measure:
            element.tag = element.tag.split("_")[1]

    reconstructed_tree: Element = ET.Element("score-partwise")
    reconstructed_tree.attrib['version'] = "2.0"

    reconstructed_tree.append(part_list)

    # Reconstruct the song
    reconstructed_part: Element = ET.Element("part")
    reconstructed_part.attrib['id'] = "P1"

    index = 1
    for measure in output:
        measure.attrib['number'] = str(index)
        reconstructed_part.append(measure)
        index += 1

    reconstructed_part.find("measure").insert(0, instruction)

    # save the reconstructed part to temp.xml
    reconstructed_tree.append(reconstructed_part)


    final_tree = ET.ElementTree(reconstructed_tree)
    return final_tree
