from pathlib import Path

from umed_modern_filter.rdf_parse import filter_dict, parse_trig
import json

def main():
    final_dict = {}
    curr = {}
    directories = list(Path("./data/gitlab/").iterdir())
    for dir in directories:
        workfile_paths = list(dir.iterdir())
        for workfile_path in workfile_paths:
            work_id = workfile_path.stem
            work_dict = parse_trig(workfile_path)
            curr[work_id] = work_dict
            final_dict.update(curr)
            curr = {}
    write_json(final_dict)
    
def write_json(data):
    with open("./data/work_info.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
