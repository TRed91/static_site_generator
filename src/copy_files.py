import os
import shutil

def copy_files(source : str, destination : str) -> None:
    
    if not os.path.exists(source):
        raise Exception("Source directory does not exist")
    
    if not os.path.exists(destination):
        raise Exception("Destination directory does not exist")
    
    clear_dir(destination)

    copy_dir_level(source, destination)


def clear_dir(dir : str) -> str:
    elements = os.listdir(dir)
    for element in elements:
        path = f"{dir}/{element}"
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

def copy_dir_level(source: str, dest: str) -> None:
    source_elements = os.listdir(source)

    for element in source_elements:
        source_path = f"{source}/{element}"
        dest_path = f"{dest}/{element}"

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"copied: {source_path} -> {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"created directory: {dest_path}")
            copy_files(source_path, dest_path)