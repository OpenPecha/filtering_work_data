import json
import os
from typing import Dict, List, Optional, Union


def traverse_and_check(
    directory_path: str,
) -> Dict[str, List[Dict[str, Union[str, Dict[str, List[Optional[str]]]]]]]:
    """
    Recursively traverses a directory containing JSON files and checks conditions within the JSON objects.

    Args:
        directory_path (str): The path to the directory containing JSON files.

    Returns:
        Dict[str, List[Dict[str, Union[str, Dict[str, List[Optional[str]]]]]]]: A dictionary containing filtered data.
            The dictionary has keys representing work IDs and values as lists of dictionaries containing filtered data.

    Example:
        {
            "work_id_1": [
                {
                    "inner_key_1": {
                        "modern_print_instance": ["instance_id_1"],
                        "umen_instance": ["instance_id_1"]
                    }
                },
                # More dictionaries with filtered data...
            ],
            # More work IDs and filtered data...
        }
    """
    filter_dict: Dict[
        str, List[Dict[str, Union[str, Dict[str, List[Optional[str]]]]]]
    ] = {}

    # Rest of your code...

    # Iterate through JSON files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)

            # Load JSON data from the file
            with open(file_path) as json_file:
                json_obj = json.load(json_file)

            for key, value_list in json_obj.items():
                for value_item in value_list:
                    if isinstance(
                        value_item, dict
                    ):  # Ensure value_item is a dictionary
                        for inner_key, inner_obj in value_item.items():
                            if isinstance(
                                inner_obj, dict
                            ):  # Ensure inner_obj is a dictionary
                                print_method_list = inner_obj.get("printMethod", [])
                                script_list = inner_obj.get("script", [])

                                # Check your conditions here
                                if (
                                    "PrintMethod_Manuscript" in print_method_list
                                    and "ScriptDbuCan" in script_list
                                ):
                                    if key not in filter_dict:
                                        filter_dict[key] = []

                                    # Check if the inner_obj already exists in the list
                                    if {
                                        inner_key: {
                                            "modern_print_instance": [
                                                inner_obj.get("instanceOf")
                                            ],
                                            "umen_instance": [
                                                inner_obj.get("instanceOf")
                                            ],
                                        }
                                    } not in filter_dict[key]:
                                        filter_dict[key].append(
                                            {
                                                inner_key: {
                                                    "modern_print_instance": [
                                                        inner_obj.get("instanceOf")
                                                    ],
                                                    "umen_instance": [
                                                        inner_obj.get("instanceOf")
                                                    ],
                                                }
                                            }
                                        )
                                        print(
                                            f"work_id: {key}, instance_id: {inner_obj.get('instanceOf')}"
                                        )
    return filter_dict


if __name__ == "__main__":
    # Directory containing JSON files
    directory_path = "../../data/json"  # Replace with your directory path
    # Start the traversal from the root of the JSON data and check conditions
    final_dict = traverse_and_check(directory_path)
    # File path to save the JSON data
    file_path = "../../data/filter_list.json"
    # Write the dictionary to a JSON file
    with open(file_path, "a") as json_file:
        json.dump(final_dict, json_file, indent=4)
