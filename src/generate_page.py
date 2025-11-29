import os
from utility_functions import markdown_to_html_node, extract_title

def generate_page(from_path : str, template_path : str, dest_path : str, basepath : str) -> None:
    
    if not os.path.exists(from_path):
        raise Exception(f"Source path does not exist {from_path}")

    if not os.path.exists(template_path):
        raise Exception(f"Template file does not exist {template_path}")
    

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        if not os.path.isfile(from_path):
            raise Exception(f"Source path is not a file: {from_path}")
        
        with open(from_path, "r") as file:
            md_content = file.read()

        with open(template_path, "r") as file:
            template_content = file.read()

        html_node = markdown_to_html_node(md_content)
        html_string = html_node.to_html()

        title = extract_title(md_content)

        html = template_content.replace("{{ Title }}", title)
        html = html.replace("{{ Content }}", html_string)

        html = html.replace('"href="/', f'href="{basepath}')
        html = html.replace('src="/', f'src="{basepath}')

        if not os.path.exists(dest_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "x") as file:
                file.write(html)
        else:
            with open(dest_path, "w") as file:
                file.write(html)


    except Exception:
        raise

