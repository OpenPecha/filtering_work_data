import os
import random
from PIL import Image
from pathlib import Path

def create_grid(images):
    # Assuming all images are of the same size
    width, height = images[0].size
    grid = Image.new('RGB', (width * 3, height * 3))
    for index, image in enumerate(images):
        grid.paste(image, ((index % 3) * width, (index // 3) * height))
    return grid

def remove_extra_images(image_paths):
    num_of_images = len(image_paths)
    if num_of_images > 9:
        sorted_images = sorted(image_paths)
        selected_image_paths = sorted_images[3:]
    else:
        return None
    for image_path in image_paths:
        if image_path not in selected_image_paths:
            os.remove(image_path)
    return selected_image_paths


def get_image_names(work_folder):
    image_paths = list(work_folder.iterdir())
    image_names = []
    if len(image_paths) != 9:
        image_paths = remove_extra_images(image_paths)
        if image_paths == None:
            return None, None
    for image_path in image_paths:
        image_name = image_path.stem[-4:]
        image_names.append(image_name)
    image_group_id = image_path.stem[:-4]
    return image_group_id, image_names

def stitch_image(dir_path, type):
    dir = (dir_path.parent).stem
    folder_path = Path(f"./script_classification/{dir}/{type}_combined")
    folder_path.mkdir(parents=True, exist_ok=True)
    for work_folder in list(dir_path.iterdir()):
        work_id = work_folder.stem
        image_group_id, image_names = get_image_names(work_folder)
        if image_names == None:
            continue
        merged_image_name = f"{work_id}_{image_group_id}"+ "_".join(image_names)
        new_image_path = Path(f"./{folder_path}/{merged_image_name}.jpg")
        if new_image_path.exists():
            continue
        images = [Image.open(x) for x in sorted(list(work_folder.iterdir()))]
        combined_image = create_grid(images)

        # Select a random image to slice
        selected_image = random.choice(images)
        width, height = selected_image.size
        left_half = selected_image.crop((0, 0, width // 2, height))

        scaled_width = left_half.width * 4
        scaled_height = left_half.height * 4

        scaled_left_half = left_half.resize((scaled_width, scaled_height), Image.LANCZOS)

        # Calculate the position to paste the scaled slice (center of the grid)
        paste_position_x = (combined_image.width - scaled_left_half.width) // 2
        paste_position_y = (combined_image.height - scaled_left_half.height) // 2

        # Paste the scaled middle slice onto the center of the grid
        combined_image.paste(scaled_left_half, (paste_position_x, paste_position_y))
        combined_image.save(new_image_path)

# if __name__ == "__main__":
#     dir_path = Path("./4f/manuscript_works")
#     stich_image(dir_path, "manuscript")
