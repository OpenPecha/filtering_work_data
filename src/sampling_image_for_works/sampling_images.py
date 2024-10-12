import json
import random
import hashlib
from pathlib import Path
from openpecha.buda.api import get_buda_scan_info, get_image_list, image_group_to_folder_name
from sampling_image_for_works.config import BDRC_ARCHIVE_BUCKET, bdrc_s3_client, bdrc_s3_session
from PIL import Image
from sampling_image_for_works.image_manipulation import stitch_image
import subprocess
import shutil


s3 = bdrc_s3_session.client('s3')
bucket_name = BDRC_ARCHIVE_BUCKET

def download_images(obj_keys, output_path):
    for obj_key in obj_keys:
        image_name = obj_key.split("/")[-1]
        output_path.mkdir(parents=True, exist_ok=True)
        image_path = output_path/image_name
        if image_path.exists():
            continue
        if len(list(output_path.iterdir())) == 9:
            break
        try:
            response = s3.get_object(Bucket=bucket_name, Key=obj_key)
            image_data = response['Body'].read()
            with open(image_path, 'wb') as f:
                f.write(image_data)
        except Exception as e:
            print(f"Error: {e}")


def get_hash(work_id):
    md5 = hashlib.md5(str.encode(work_id))
    two = md5.hexdigest()[:2]
    return two


def remove_non_page(images_list, scan_id, image_group_id):
    s3_keys = []
    hash_two = get_hash(scan_id)
    for image in images_list[5:]:
        imagegroup = image_group_to_folder_name(scan_id, image_group_id)
        s3_key = f"Works/{hash_two}/{scan_id}/images/{imagegroup}/{image['filename']}"
        s3_keys.append(s3_key)
    return s3_keys


def get_image_paths(scan_id):
    scan_info = get_buda_scan_info(scan_id)
    if scan_info == None:
        return None
    elif scan_info["image_groups"] == {}:
        return None
    for image_group_id, _ in scan_info["image_groups"].items():
        images_s3_keys = []
        try:
            images_list = get_image_list(scan_id, image_group_id)
            if images_list == None:
                return None
            images_s3_keys = remove_non_page(images_list, scan_id, image_group_id)
            if len(images_s3_keys) < 10:
                return None
            sample_images_keys = list(random.sample(images_s3_keys, 9))
            break
        except Exception as e:
            print(f"Error: {e}")
            sample_images_keys = []
    return sample_images_keys


def get_sample_images(instance_ids, data_dir):
    for instance_id in instance_ids:
        scan_id = instance_id[1:]
        output_path = Path(f"{data_dir}/{scan_id}")
        if Path(f"./error_data/{scan_id}").exists() and not output_path.exists():
            subprocess.run(["cp", "-rf", str(f"./error_data/{scan_id}"), str(output_path)])
            continue
        if output_path.exists():
            continue
        else:
            images_paths = get_image_paths(scan_id)
            if images_paths == None:
                print(f"info for {scan_id} not found")
                continue
            download_images(images_paths, output_path)



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
                else:
                    print(f"{printMethod} not in the list")
    return manuscript, woodblock


def get_image_names(image_paths):
    image_names = []
    for image_path in image_paths:
        image_name = image_path.stem[-4:]
        image_names.append(image_name)
    image_group_id = image_path.stem[:-4]
    return image_group_id, image_names


def copy_images(work_paths, new_dir):
    for work_path in work_paths:
        new_path = new_dir/work_path.stem
        if new_path.exists():
            continue
        else:
            subprocess.run(["cp", "-rf", str(work_path), str(new_dir)])

def merge_all_works():
    new_woodblock_dir = Path(f"./data/woodblock_works")
    new_manuscript_dir = Path(f"./data/manuscript_works")
    class_paths = Path(f"./script_classification").iterdir()
    for class_path in class_paths:
        if (class_path/"woodblock_works").exists():
            woodblock_work_paths = list((class_path/"woodblock_works").iterdir())
            copy_images(woodblock_work_paths, new_woodblock_dir)
        if (class_path/"manuscript_works").exists():
            manuscript_work_paths = list((class_path/"manuscript_works").iterdir())
            copy_images(manuscript_work_paths, new_manuscript_dir)


def clean_empty_dirs():
    manusscript_dir_works = list(Path(f"./data/manuscript_works").iterdir())
    for work in manusscript_dir_works:
        if len(list(work.iterdir())) == 0:
            work.rmdir()
    woodblock_dir_works = list(Path(f"./data/woodblock_works").iterdir())
    for work in woodblock_dir_works:
        if len(list(work.iterdir())) == 0:
            work.rmdir()

def main():
    # merge_all_works()
    # clean_empty_dirs()
    json_paths = list(Path("data/json").iterdir())
    for json_path in json_paths[138:]:
        file_name = json_path.stem
        print(f"processing {file_name}")
        manuscript_path = Path(f"./data/manuscript_works")
        woodblock_path = Path(f"./data/woodblock_works")
        manuscript_work_ids, woodblock_work_ids = get_non_modern_works(json_path)
        get_sample_images(manuscript_work_ids, manuscript_path)
        get_sample_images(woodblock_work_ids, woodblock_path)



if __name__ == "__main__":
    main()
