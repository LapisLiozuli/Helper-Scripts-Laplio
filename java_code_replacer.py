# -*- coding: utf-8 -*-
"""
Filename: java_code_replacer.py
Date created: Thu Nov 19 11:28:44 2020
@author: Julio Hong
Purpose: I paste code into a text file and this will replace a single variable with the input string.
Steps: 
1. Input string
2. Text file automatically opens.
3. Paste the code into IntelliJ which will automatically add indents.
4. Add whatever other changes to the code
5. Close the output file so the script can access it again. 
(Not actually necessary as a dialog box will ask to reload.)
For colours, light blue and light gray are a bit troublesome, but not worth accounting for yet.
"""
from os import startfile

# Use mass_replace_code()
address_input = r"C:\Users\Julio Hong\Documents\LapisLiozuli\java_code_input.txt"
address_output = r"C:\Users\Julio Hong\Documents\LapisLiozuli\java_code_output.txt"
dye_colours = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
               'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
dye_colours_ch_zn = ['白色', '橙色', '品红色', '淡蓝色', '黃色', '黄绿色', '粉紅色', '灰色',
               '淡灰色', '青色', '紫色', '藍色', '棕色', '绿色', '紅色', '黑色']

# Replaces a single debug string with as a new colour string
def read_and_replace_colour(colour):
    reading_file = open(address_input, "r")
    
    new_file_content = ""
    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line.replace("debug", colour.lower())
        new_line = new_line.replace("Debug", colour.capitalize())
        new_line = new_line.replace("DEBUG", colour.upper())
        new_file_content += new_line +"\n"
    reading_file.close()
    
    return new_file_content

# Replaces a single debug file with as a new colour file
def replace_sec_in_class(colour):
    new_file_content = read_and_replace_colour(colour)
   # reading_file = open(address_input, "r")
   #
   # new_file_content = ""
   # for line in reading_file:
   #     stripped_line = line.strip()
   #     new_line = stripped_line.replace("debug", colour.lower())
   #     new_line = new_line.replace("Debug", colour.capitalize())
   #     new_line = new_line.replace("DEBUG", colour.upper())
   #     new_file_content += new_line +"\n"
   # reading_file.close()

    writing_file = open(address_output, "w")
    writing_file.write(new_file_content)
    writing_file.close()
    
    startfile(address_output) 

# Replaces a single debug template with as many lines as there are colours
def mass_replace_code():
    # For short pieces of code
    mass_nfc = []
    for colour in dye_colours:
        new_file_content = read_and_replace_colour(colour)
#        reading_file = open(address_input, "r")
#    
#        new_file_content = ""
#        for line in reading_file:
#            stripped_line = line.strip()
#            new_line = stripped_line.replace("debug", colour.lower())
#            new_line = new_line.replace("Debug", colour.capitalize())
#            new_line = new_line.replace("DEBUG", colour.upper())
#            new_file_content += new_line +"\n"
#        reading_file.close()
        
        # I need to incrementally add to new_file_content instead of overwriting.
        mass_nfc.append(new_file_content)
    
#    new_mass_content = mass_nfc.join("\n")
    new_mass_content = "".join(mass_nfc)
    
    writing_file = open(address_output, "w")
    writing_file.write(new_mass_content)
    writing_file.close()
    
    startfile(address_output) 
    
    
import re

# Trying to retain formatting
INDENT_RE = re.compile(r'^\s*$')
# https://stackoverflow.com/questions/26683175/how-can-i-keep-the-indentation-between-lines
def matching_indent(line, pattern):
    """
    Returns indent if line matches pattern, else returns None.
    """
    if line.endswith(pattern):
        indent = line[:-len(pattern)]
        if INDENT_RE.match(indent):
            return indent
    return None

def replace_line(lines, pattern, replacements):
    for line in lines:
        indent = matching_indent(line, pattern)
        if indent is None:
            yield line
        else:
            for replacement in replacements:
                yield indent + replacement
