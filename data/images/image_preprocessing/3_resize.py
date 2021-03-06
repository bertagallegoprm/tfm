import os
import errno
import shutil
from PIL import Image
from data.config import resizing
from data.image import ImageDimension


def create_empty_dir(base_path, directory):
    """
    Create a new directory.
    If it already exists, it deletes it and all its contents.
    It returns the new directory path.
    """
    full_path = base_path + directory
    print(f"Creating directory: {full_path}")
    try:
        shutil.rmtree(full_path)
    except:
        pass
    finally:
        os.mkdir(full_path)
        print (f"Created directory {full_path}.")
        return full_path


def resize_image(source_dir, destination_dir, image_file, new_size):
    """
    """
    try:
        image = Image.open(os.path.join(source_dir, image_file))  
        try:
            image = image.resize(new_size)
            try:
                if not os.path.exists(destination_dir):
                    os.mkdir(destination_dir)
                image = image.save(os.path.join(destination_dir,image_file)) 
            except: 
                return print(f"Unable to save image {image_file}.")
        except:
            return print(f"Unable to resize image {image_file}.")
    except:
        print(f"Unable to open image {image_file}.")
    
     
    

def resize_all_images(source_dir, destination_dir, new_size):
    """
    Apply crop_image() to every image in the source directory.
    The source directory must have subfolders for each of the classes.
    """
    if os.path.exists(source_dir):
        for species_folder in os.listdir(source_dir):
            for image_file in os.listdir(os.path.join(source_dir, species_folder)):
                resize_image(os.path.join(source_dir, species_folder), 
                             os.path.join(destination_dir, species_folder), 
                             image_file,
                             new_size)
    else:
        print(f"Folder {source_dir} not found.")
    print("End.")




if __name__ == "__main__":

    # SOURCE DIR
    source_dir = "data/images/raw_images/"

    # DESTINATION DIR
    base_path = "data/images/image_preprocessing/"
    directory = "resized_images"
    destination_dir = create_empty_dir(base_path, directory)

    # Resize
    new_size = resizing.image_size()
    resize_all_images(source_dir, destination_dir, new_size)