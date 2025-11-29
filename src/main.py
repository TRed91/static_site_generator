import sys
from generate_pages import generate_pages_recursive
from copy_files import copy_files

def main():

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
   
    copy_files("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()