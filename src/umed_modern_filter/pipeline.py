import json
from pathlib import Path

from umed_modern_filter.rdf_parse import parse_trig


def main():
    final_dict = {}
    curr = {}
    directories = list(Path("../../data/gitlab/").iterdir())
    for dir in directories:
        workfile_paths = list(dir.iterdir())
        for workfile_path in workfile_paths:
            work_id = workfile_path.stem
            work_dict = parse_trig(workfile_path)
            curr[work_id] = work_dict
            final_dict.update(curr)
            curr = {}
        dir_name = dir.name
        write_json(final_dict, dir_name)


def write_json(data, dir_name):
    file_path = Path(f"../../data/json/{dir_name}.json")
    if not file_path.exists():
        with file_path.open("w") as json_file:
            json.dump(data, json_file, indent=4)
    else:
        print("The JSON file already exists. You can choose to update or overwrite it.")


if __name__ == "__main__":
    main()
