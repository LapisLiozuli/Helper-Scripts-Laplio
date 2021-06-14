# -*- coding: utf-8 -*-
"""
Filename: biome_sec_swapper.py
Date created: Fri Jun  4 00:08:21 2021
@author: Julio Hong
Purpose: Swap from Biome:Colour format to Colour:Biome format.
Steps:
The functions keep returning huge dicts so maybe tidy up tomorrow.

"""
from os import startfile
import ast
import pickle
import json

# Use mass_replace_code()
address_input = r"C:\Users\Julio Hong\Documents\LapisLiozuli\biome_to_sec.txt"
# address_output = r"C:\Users\Julio Hong\Documents\LapisLiozuli\biome_to_sec.json"
# Separate output to avoid overwriting address_input.
address_output = r"C:\Users\Julio Hong\Documents\LapisLiozuli\biome_to_sec2.txt"
swapped_output = r"C:\Users\Julio Hong\Documents\LapisLiozuli\sec_to_biome.txt"

dye_colours = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
               'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']

# https://stackoverflow.com/questions/13809628/how-to-read-dictionary-data-from-a-file-in-python
# Open Biome:Colour dict from text file.
with open(address_input,'r') as text_input:
    # Using ast raises an error...
    # biome_to_sec_dict = ast.literal_eval(text_input.read())
    # Using eval has security issues.
    biome_to_sec_dict = eval(text_input.read())

# # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
# # JSON Decode Error.
# with open(address_input) as text_input:
#     # Type of text_data is string
#     text_data = text_input.read()
#     # Type of text_data is dict
#     biome_to_sec_dict = json.loads(text_data)

# # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
# # Reading the data from the file.
# # Would be nice to consistently use Pickle for both file reading and writing.
# # Error raised: Invalid load key.
# with open(address_input, 'rb') as text_input:
#     # Type of text_data is bytes
#     text_data = text_input.read()
#     # Reconstructing text_data as dictionary
#     biome_to_sec_dict = pickle.loads(text_data)

# Reorders the colour lists (values) in address_input according to dye_colours.
def read_and_reorder_colours():
    # Get the colour list for each biome.
    for biome in biome_to_sec_dict:
        # List comprehension over dye_colours keeps order, while checking if colour is present in colour-list.
        biome_to_sec_dict[biome] = [x for x in dye_colours if x in biome_to_sec_dict[biome]]
    return biome_to_sec_dict

# Saves the dict back to the text file, with each key-value (k-v) pair on a newline.
# This loop worked perfectly.
def line_by_line(raw_dict, output_path):
    f = open(output_path, "w")
    f.write("{\n")
    for k in raw_dict.keys():
        f.write("'{}':{}\n".format(k, raw_dict[k]))
    f.write("}")
    f.close()


def line_by_line2(raw_dict, output_path):
    f = open(output_path, "w")
    f.write("{\n")
    for k in raw_dict.keys():
        spacer = ", "
        entry = spacer.join(raw_dict[k])
        # Find a way to insert " character without breaking everything. Or I can replace in Notepad++
        f.write("'{}':'{}';\n".format(k, entry))
    f.write("}")
    f.close()

# # Uses JSON lib.
# # https://stackoverflow.com/questions/10183453/adding-a-n-to-the-end-of-my-dictionary-when-writing-it-to-file
# # Might improve with this?
# def export_dict():
#     a_file = open(address_output, "w")
#     json.dump(biome_to_sec_dict, a_file)
#     a_file.close()

# # This function messed up the formatting greatly.
# def save_dict():
#     # opening file in write mode (binary)
#     file = open(address_input, "wb")
#     # serializing dictionary
#     pickle.dump(biome_to_sec_dict, file)
#     # closing the file
#     file.close()

# Create Colour:Biome dict using dye_colours as keys.
sec_to_biome_dict = dict.fromkeys(dye_colours)
# Iterate over biome_to_sec_dict. If the entry contains the colour, add the biome (key) to the new dict.
def swap_the_kvs():
    # Iterate over each colour.
    for colour in sec_to_biome_dict:
        # Check each biome.
        for biome in biome_to_sec_dict:
            # Check if the SEC can spawn in this biome.
            if colour in biome_to_sec_dict[biome]:
                # Check if a list already exists.
                if sec_to_biome_dict[colour] == None:
                    sec_to_biome_dict[colour] = [biome]
                else:
                    sec_to_biome_dict[colour].append(biome)

    return sec_to_biome_dict


# Execute these functions.
biome_to_sec_dict = read_and_reorder_colours()
sec_to_biome_dict = swap_the_kvs()
# line_by_line(biome_to_sec_dict, address_output)
# line_by_line2(sec_to_biome_dict, swapped_output)