import math
import os
import shutil
import tempfile
import zipfile
from io import StringIO
from typing import Any, Dict, List, Tuple
from xml.etree.ElementTree import Element, ElementTree

import lxml.etree as ET
import xmltodict
import yaml
from lxml import etree
from transformers import AutoTokenizer


def unzip_file(mxl_file, temp_file):
    with zipfile.ZipFile(mxl_file, "r") as zip_ref:
        zip_ref.extractall(temp_file)
    return temp_file


def element_deleter(root: Element, element_name: str) -> None:
    element_to_delete = root.find(element_name)

    while element_to_delete is not None:
        root.remove(element_to_delete)
        element_to_delete = root.find(element_name)


def attribute_deleter(element: Element, attribute_name: str) -> None:
    if attribute_name in element.attrib:
        del element.attrib[attribute_name]


font_array = [
    "font-family",
    "font-size",
    "font-style",
    "font-weight",
]

core_attributes = [
    "default-y",
    "default-x",
    "color",
    "id",
]

relative_print = [
    "print-object",
    "relative-x",
    "relative-y",
]

score_partwise_removed_elements = [
    "work",
    "movement-number",
    "movement-title",
    "identification",
    "defaults",
    "credit",
    "part-list",
]

score_partwise_kept_elements = ["part"]

score_partwise_removed_attributes = [
    "version",
]

score_partwise_dict = {
    "removed_elements": score_partwise_removed_elements,
    "kept_elements": score_partwise_kept_elements,
    "removed_attributes": score_partwise_removed_attributes,
    "kept_attributes": [],
}

part_kept_elements = [
    "measure",
]

part_removed_attributes = [
    "id",
]

part_dict = {
    "removed_elements": [],
    "kept_elements": part_kept_elements,
    "removed_attributes": part_removed_attributes,
    "kept_attributes": [],
}

measure_removed_elements = [
    "print",
    "direction",
    "barline",
]

measure_kept_elements = [
    "attributes",
    "note",
    "backup",
    "forward",
    "harmony",
    "sound",
]

measure_removed_attributes = [
    "width",
    "implicit",
    "number",
    "id",
    "implicit",
    "text",
    "non-controlling",
]

measure_dict = {
    "removed_elements": measure_removed_elements,
    "kept_elements": measure_kept_elements,
    "removed_attributes": measure_removed_attributes,
    "kept_attributes": [],
}

attributes_removed_elements = [
    "staff-details",
]

attributes_kept_elements = [
    "divisions",  # No elements or attributes inside
    "key",
    "time",
    "clef",
    "transpose",
    "staves",  # Used to determine if the part should be discarded later
    "measure-style",
]

attributes_dict = {
    "removed_elements": attributes_removed_elements,
    "kept_elements": attributes_kept_elements,
    "removed_attributes": [],
    "kept_attributes": [],
}

key_kept_elements = [
    "fifths",
]

key_removed_attributes = (
    [
        "number",
    ]
    + font_array
    + core_attributes
    + relative_print
)

key_dict = {
    "removed_elements": [],
    "kept_elements": key_kept_elements,
    "removed_attributes": key_removed_attributes,
    "kept_attributes": [],
}

time_kept_elements = [
    "beats",
    "beat-type",
]

time_removed_attributes = (
    [
        "halign",
        "separator",
        "symbol",
        "valign",
    ]
    + font_array
    + core_attributes
    + relative_print
)

time_dict = {
    "removed_elements": [],
    "kept_elements": time_kept_elements,
    "removed_attributes": time_removed_attributes,
    "kept_attributes": [],
}

clef_kept_elements = [
    "sign",
    "line",
]

clef_removed_attributes = (
    ["additional", "after-barline", "number", "size"]
    + font_array
    + core_attributes
    + relative_print
)

clef_dict = {
    "removed_elements": [],
    "kept_elements": clef_kept_elements,
    "removed_attributes": clef_removed_attributes,
    "kept_attributes": [],
}

note_removed_elements = [
    "lyric",
    "stem",
    "voice",
    "beam",
    "notations",  # Only used for visual clarity
    "instrument",  # We will always use the same instrument
    "notehead",
]

note_kept_elements = [
    "pitch",
    "duration",  # No elements or attributes inside
    "type",
    "chord",  # No elements or attributes inside
    "accidental",
    "rest",
    "dot",
    "tie",
    "time-modification",
    "staff",  # Doesn't really matter if it's kept, used with stave
    "unpitched",
    "grace",
    "cue",
]

note_removed_attributes = (
    ["dynamics", "end-dynamics"] + font_array + core_attributes + relative_print
)

note_kept_attributes = [
    "release",
    "attack",
]

note_dict = {
    "removed_elements": note_removed_elements,
    "kept_elements": note_kept_elements,
    "removed_attributes": note_removed_attributes,
    "kept_attributes": note_kept_attributes,
}

pitch_kept_elements = [
    "step",  # No elements or attributes inside
    "octave",  # No elements or attributes inside
]

pitch_dict = {
    "removed_elements": [],
    "kept_elements": pitch_kept_elements,
    "removed_attributes": [],
    "kept_attributes": [],
}

accidental_removed_attributes = (
    [
        "bracket",
        "cautionary",
        "editorial",
        "parentheses",
        "size",
        "smufl",
    ]
    + font_array
    + core_attributes
    + relative_print
)

accidental_dict = {
    "removed_elements": [],
    "kept_elements": [],
    "removed_attributes": accidental_removed_attributes,
    "kept_attributes": [],
}

rest_kept_elements = [
    "display-step",  # No elements or attributes inside
    "display-octave",  # No elements or attributes inside
]

rest_kept_attributes = ["measure"]

rest_dict = {
    "removed_elements": [],
    "kept_elements": rest_kept_elements,
    "removed_attributes": [],
    "kept_attributes": rest_kept_attributes,
}

dot_kept_attributes = ["placement"] + font_array + core_attributes + relative_print

dot_dict = {
    "removed_elements": [],
    "kept_elements": [],
    "removed_attributes": [],
    "kept_attributes": dot_kept_attributes,
}

tie_kept_attributes = [
    "type",
]

tie_dict = {
    "removed_elements": [],
    "kept_elements": [],
    "removed_attributes": [],
    "kept_attributes": tie_kept_attributes,
}

time_modification_kept_elements = ["actual-notes", "normal-notes"]

time_modification_dict = {
    "removed_elements": [],
    "kept_elements": time_modification_kept_elements,
    "removed_attributes": [],
    "kept_attributes": [],
}

harmony_removed_elements = [
    "footnote",
    "level",
]

harmony_kept_elements = [
    "root",
    "numeral",
    "function",
    "kind",
    "inversion",
    "bass",
    "degree",
    "offset",
    "frame",
    "staff",
]

harmony_removed_attributes = (
    ["placement", "print-frame", "system"]
    + font_array
    + core_attributes
    + relative_print
)

harmony_dict = {
    "removed_elements": harmony_removed_elements,
    "kept_elements": harmony_kept_elements,
    "removed_attributes": harmony_removed_attributes,
    "kept_attributes": [],
}


def element_cleaner(element: Element, element_dict: dict) -> Element:
    for attribute_name in element.attrib:
        if attribute_name in element_dict["removed_attributes"]:
            attribute_deleter(element, attribute_name)
        elif attribute_name not in element_dict["kept_attributes"]:
            raise ValueError(
                "Found the attribute: {} in {}".format(attribute_name, element.tag)
            )
    for child in element:
        if child.tag in element_dict["removed_elements"]:
            element_deleter(element, element_name=child.tag)
        elif child.tag not in element_dict["kept_elements"]:
            raise ValueError(
                "Found the element: {} in {}".format(child.tag, element.tag)
            )


def music_xml_cleaner(score_partwise: Element) -> Element:

    element_cleaner(score_partwise, score_partwise_dict)
    element_cleaner(score_partwise, score_partwise_dict)

    for part in score_partwise:
        element_cleaner(part, part_dict)
        for measure in part:
            element_cleaner(measure, measure_dict)
            for element in measure:
                if element.tag == "note":
                    element_cleaner(element, note_dict)
                    for note_element in element:
                        if element.tag == "pitch":
                            element_cleaner(element, pitch_dict)
                        elif element.tag == "accidental":
                            element_cleaner(element, accidental_dict)
                        elif element.tag == "rest":
                            element_cleaner(element, rest_dict)
                        elif element.tag == "dot":
                            element_cleaner(element, dot_dict)
                        elif element.tag == "tie":
                            element_cleaner(element, tie_dict)
                        elif element.tag == "time-modification":
                            element_cleaner(element, time_modification_dict)
                elif element.tag == "harmony":
                    element_cleaner(element, harmony_dict)
                elif element.tag == "attributes":
                    element_cleaner(element, attributes_dict)
    return score_partwise


def clean_file(file) -> Tuple[Element, ElementTree]:
    tree: ElementTree = ET.parse(file)
    root: Element = tree.getroot()

    part_list = root.find("part-list")

    cleaned_root = music_xml_cleaner(root)
    cleaned_root = music_xml_cleaner(cleaned_root)
    cleaned_root = music_xml_cleaner(cleaned_root)
    cleaned_tree = ET.ElementTree(cleaned_root)
    return part_list, cleaned_tree


def index_elements(tree: ElementTree) -> ElementTree:
    root: Element = tree.getroot()

    for measure in root:
        index = 0
        for element in measure:
            if element.tag == "attributes":
                continue
            element.tag = f"a{index:02d}" + "_" + element.tag
            index += 1

    new_tree: ElementTree = ET.ElementTree(root)
    return new_tree


def music_xml_to_inputs(document) -> Tuple[Element, str, str]:
    part_list, document_tree = clean_file(document)

    root: Element = document_tree.getroot()
    part: Element = root.find("part")
    new_tree: ElementTree = ET.ElementTree(part)

    new_tree = index_elements(new_tree)
    xml_string = ET.tostring(new_tree, encoding="UTF-8")
    document_dict = xmltodict.parse(xml_string)

    instruction_dict = document_dict["part"]["measure"][0]["attributes"]
    del document_dict["part"]["measure"][0]["attributes"]

    input_dict = document_dict["part"]["measure"]

    instruction_yaml = yaml.dump(instruction_dict)
    input_yaml = yaml.dump(input_dict)

    return part_list, instruction_yaml, input_yaml
