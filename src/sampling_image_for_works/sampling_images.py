from pathlib import Path
import json


def download_images(scan_id, image_paths):
    pass


def get_image_paths(scan_id):
    pass


def get_ten_images(instance_ids, type):
    for instance_id in instance_ids:
        scan_id = instance_id[1:]
        images_paths = get_image_paths(scan_id)
        download_images(scan_id, images_paths, type)



def get_non_modern_works(json_path):
    manuscript = []
    woodblock = []
    data = json.load(json_path.open())
    for _, work_info in data.items():
        if work_info == []:
            continue
        for instance_id, instance_info in work_info[0].items():
            if instance_info == None:
                continue
            if "_" in instance_id:
                continue
            for printMethod in instance_info["printMethod"]:
                if printMethod == "PrintMethod_Modern":
                    continue
                elif printMethod == "PrintMethod_Manuscript":
                    manuscript.append(instance_id)
                elif printMethod == "PrintMethod_Relief_WoodBlock":
                    woodblock.append(instance_id)
    return manuscript, woodblock

def main():
    json_paths = Path("data/json").iterdir()
    for json_path in json_paths:
        manuscript, woodblock = get_non_modern_works(json_path)
        get_ten_images(manuscript, "manuscript")
        get_ten_images(woodblock, "woodblock")



if __name__ == "__main__":
    main()
