import os
import zipfile
from pathlib import Path
import shutil


def traverse_path_and_unzip(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                # Define the dir to extract to (can be adjusted as needed)
                extract_dir = root
                print(f"Extracting {zip_path} to {extract_dir}")
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"Finished extracting {file}")


def test_traverse_path_and_unzip():
    # Function to create a nested folder and a zip file within it
    def create_folder_and_zip(folder_name, zip_name, file_name):
        # Create a nested folder
        os.makedirs(folder_name, exist_ok=True)

        # Define the path for the zip file and the text file
        zip_path = os.path.join(folder_name, zip_name)
        txt_path = os.path.join(folder_name, file_name)

        # Create an empty text file
        with open(txt_path, "w") as fp:
            pass  # Create an empty file

        # Create a zip file and add the text file to it
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(txt_path, arcname=file_name)

        # Remove the text file as it's now zipped
        os.remove(txt_path)

    create_folder_and_zip("/tmp/testfolder/", "archive1.zip", "blah.txt")
    create_folder_and_zip("/tmp/testfolder/nested1", "archive1.zip", "blah.txt")
    create_folder_and_zip("/tmp/testfolder/nested2", "archive2.zip", "blah.txt")
    create_folder_and_zip("/tmp/testfolder/nested2/nested3", "archive1.zip", "blah.txt")

    traverse_path_and_unzip("/tmp/testfolder")
    assert Path("/tmp/testfolder/blah.txt").is_file()
    assert Path("/tmp/testfolder/nested1/blah.txt").is_file()
    assert Path("/tmp/testfolder/nested2/blah.txt").is_file()
    assert Path("/tmp/testfolder/nested2/nested3/blah.txt").is_file()
    shutil.rmtree("/tmp/testfolder")
