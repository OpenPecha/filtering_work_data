import json
import os


# Function to recursively traverse a JSON object and check conditions
def traverse_and_check(json_obj, parent_key=None):
    filter_dict = {}
    if isinstance(json_obj, dict):
        if "printMethod" in json_obj and "script" in json_obj:
            # Ensure that json_obj.get("printMethod") and json_obj.get("script") are not None
            print_method_list = json_obj.get("printMethod", [])
            script_list = json_obj.get("script", [])

            # Check if "PrintMethod_Modern" is in print_method_list
            # and "ScriptDbuMed" is in script_list
            if (
                "PrintMethod_Modern" in print_method_list
                and "ScriptDbuMed" in script_list
            ):
                print(
                    f"work_id: {parent_key}, instance_id: {json_obj.get('instanceOf')}"
                )
                filter_dict[parent_key] = {
                    "modern_print_instance": [json_obj.get("instanceOf")],
                    "umen_instance": [json_obj.get("instanceOf")],
                }
                # File path to save the JSON data
                file_path = "../../data/filter_list.json"
                # Write the dictionary to a JSON file
                with open(file_path, "a") as json_file:
                    json.dump(filter_dict, json_file, indent=4)
        for key, value in json_obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            traverse_and_check(value, new_key)
    elif isinstance(json_obj, list):
        for item in json_obj:
            new_key = parent_key
            traverse_and_check(item, new_key)


if __name__ == "__main__":
    # Directory containing JSON files
    directory_path = "../../data/json/"  # Replace with your directory path

    # Iterate through JSON files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)

            # Load JSON data from the file
            with open(file_path) as json_file:
                json_data = json.load(json_file)

            # Start the traversal from the root of the JSON data and check conditions
            traverse_and_check(json_data)
