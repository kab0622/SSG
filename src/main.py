from textnode import TextNode, TextType
import os
import shutil
from generate_page import generate_page, generate_pages_recursive

def sync_directories(source, destination):
    def delete_files(target_dir):
        if not os.path.exists(target_dir):
            return
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isdir(item_path):
                delete_files(item_path)
                os.rmdir(item_path)
            else:
                os.remove(item_path)
    
    def copy_files(source, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)

        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            destination_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                copy_files(source_item, destination_item)
            else:
                shutil.copy(source_item, destination_item)
    print("recursively deleting")
    delete_files(destination)
    if os.path.exists(source):
        print("recursively copying")
        copy_files(source, destination)

def main():
    source = "./static"
    destination = "./public"

    sync_directories(source, destination)

    generate_pages_recursive("./content", "./template.html", "./public")

main()