import os
from typing import Dict, List

from umed_modern_filter.rdf_parse import parse_trig_file


def pretty_print_dict(d: Dict, indent: int = 0):
    for key, value in d.items():
        if isinstance(value, dict):
            print("  " * indent + str(key) + ":")
            pretty_print_dict(value, indent + 3)
        else:
            print("  " * indent + str(key) + ": " + str(value))


def create_dictionary(
    root_directory: str,
) -> Dict[str, Dict[str, Dict[str, List[str]]]]:

    data_dict = {}

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            trig_file_path = os.path.join(root, file)
            if file.endswith(".trig"):
                try:
                    result = parse_trig_file(trig_file_path)
                    data_dict.update(result)
                except Exception as e:
                    print(f"Error in file {trig_file_path}: {e}")

    return data_dict


if __name__ == "__main__":
    root_directory = "/home/gangagyatso/Desktop/experiment"
    data_dictionary = create_dictionary(root_directory)
    pretty_print_dict(data_dictionary)
    print(len(data_dictionary))
