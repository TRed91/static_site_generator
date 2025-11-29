import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content : str, template_path : str, dest_dir_path : str):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Content directory does not exist: {dir_path_content}")
    if not os.path.exists(template_path) or os.path.isdir(template_path):
        raise Exception(f"Template file does not exist: {template_path}")
    
    try:

        content = os.listdir(dir_path_content)

        for element in content:
            source_path = os.path.join(dir_path_content, element)
            dest_path = os.path.join(dest_dir_path, element)

            if os.path.isfile(source_path):
                dest_path = __filename_md_to_html(dest_path)
                generate_page(source_path, template_path, dest_path)
            else:
                if not os.path.exists(dest_path):
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_pages_recursive(source_path, template_path, dest_path)
    
    except Exception:
        raise

def __filename_md_to_html(md): 
    return f"{md[:-2]}html"