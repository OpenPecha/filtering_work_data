import random
from PIL import Image
from pathlib import Path


def load_image(filepath):
    """Load an image from a file."""
    return Image.open(filepath)

def crop_square(image):
    """Crop a square from the middle of the image based on its height."""
    width, height = image.size
    center_x, center_y = width // 2, height // 2
    half_height = height // 2
    left = max(center_x - half_height, 0)
    right = min(center_x + half_height, width)
    top = max(center_y - half_height, 0)
    bottom = min(center_y + half_height, height)
    return image.crop((left, top, right, bottom))

def remove_top_25_percent(image):
    """Remove the top 25% of the image."""
    width, height = image.size
    return image.crop((0, height * 0.25, width, height))

def cut_horizontally_and_stitch(image1, image2):
    """Cut two images horizontally from the middle and stitch them together."""
    width1, height1 = image1.size
    width2, height2 = image2.size

    upper_half_image1 = image1.crop((0, 0, width1, height1 // 2))
    upper_half_image2 = image2.crop((0, 0, width2, height2 // 2))

    result_image = Image.new('RGB', (max(width1, width2), height1 // 2 + height2 // 2))
    result_image.paste(upper_half_image1, (0, 0))
    result_image.paste(upper_half_image2, (0, height1 // 2))

    return result_image

def resize_to_25cm_square(image, cm_to_pixel_ratio):
    """Resize the image to fill a 25 cm square."""
    size_in_pixels = int(25 * cm_to_pixel_ratio)
    return image.resize((size_in_pixels, size_in_pixels), Image.Resampling.LANCZOS)


def create_sample_image(image_paths, image_name):
    image1 = load_image(image_paths[0])
    image2 = load_image(image_paths[1])
    cm_to_pixel_ratio = 37.7952755906
    cropped_image1 = crop_square(image1)
    sample_image1 = remove_top_25_percent(cropped_image1)
    cropped_image2 = crop_square(image2)
    sample_image2 = remove_top_25_percent(cropped_image2)
    combined_image = cut_horizontally_and_stitch(sample_image1, sample_image2)
    final_image = resize_to_25cm_square(combined_image, cm_to_pixel_ratio)
    final_image.save(f'{image_name}.jpg')

def get_image_names(work_folder):
    image_paths = list(work_folder.iterdir())
    image_names = []
    selected_image_paths = (random.sample(image_paths, 2))
    for image_path in selected_image_paths:
        image_name = image_path.stem[-4:]
        image_names.append(image_name)
    image_group_id = image_path.stem[:-4]
    return selected_image_paths, image_group_id, image_names

def get_manuscript_images(manuscript_work_paths):
    for manuscript_work_path in manuscript_work_paths:
            work_id = manuscript_work_path.stem
            image_paths, image_group_id, image_names = get_image_names(manuscript_work_path)
            new_image_name = f"{work_id}_{image_group_id}_"+ "_".join(image_names)
            create_sample_image(image_paths, f"./stitched_images/manuscript_images/{new_image_name}")

def get_woodblock_images(woodblock_work_paths):
    for woodblock_work_path in woodblock_work_paths:
            work_id = woodblock_work_path.stem
            image_paths, image_group_id, image_names = get_image_names(woodblock_work_path)
            new_image_name = f"{work_id}_{image_group_id}_"+ "_".join(image_names)
            create_sample_image(image_paths, f"./stitched_images/woodblock_images/{new_image_name}")

def main():
    dirs = list(Path(f"./script_classification").iterdir())
    for dir in dirs:
        if Path(f"{dir}/manuscript_works").exists():
            manuscript_work_paths = list(Path(f"{dir}/manuscript_works").iterdir())
            get_manuscript_images(manuscript_work_paths)
        if Path(f"{dir}/woodblock_works").exists():  
            woodblock_work_paths = list(Path(f"{dir}/woodblock_works").iterdir())
            get_woodblock_images(woodblock_work_paths)
        

if __name__ == "__main__":
    main()
