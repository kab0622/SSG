from markdown_blocks import markdown_to_html_node
from extract_title import extract_title
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    template_file = open(template_path, "r")
    template= template_file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_path):
            old_file = Path(dest_path)
            new_file = old_file.with_suffix(".html")
            generate_page(source_path, template_path, new_file, basepath)
        else:
            generate_pages_recursive(source_path, template_path, dest_path, basepath)