# -*- coding: utf-8 -*-
"""
Filename: fabric_json_creator.py
Date created: Mon Nov 2 23:37:44 2020
@author: Julio Hong
Purpose: Automate the creation and placement of multiple JSONs for addition of content to Minecraft Fabric mod
        Specifically, for dyed blocks which can get quite tedious.
Steps:
1. Determine the class to add.
2. Find the relevant directories for each class.
3. Design format for each type of JSON.

Initialise list of dye colours

Resources folder structure
    • Assets
        ◦ Blockstates
        ◦ Lang (Or just automatically generate the entry with a placeholder string)
        ◦ Models (Singular)
            ▪ Block
            ▪ Item / BlockItem
        ◦ Textures (Plural)
            ▪ Blocks
            ▪ Items
            ▪ Entities
    • Data
        ◦ Advancements
        ◦ Loot Table
            ▪ Blocks
            ▪ Entities
        ◦ Recipes
        ◦ Tags
"""
from os import path, remove
import pathlib
# from os import listdir
from shutil import move, copy
from copy import deepcopy
import json


# Setting up relevant filepaths
# ========================================
# The main\resources folder
template_path = r"C:\Users\Julio Hong\Documents\LapisLiozuli\laplio-template-mod"
output_path = r"C:\Users\Julio Hong\Documents\LapisLiozuli\Warehouse-Exhibition-MC"
resources_path = r"src\main\resources"
template_modid = "modid"
output_modid = "warex"

# This arrangement allows me to add new folders in future.
# The main\resources\assets folder
assets_path = path.join(resources_path, "assets")
# Final paths.
# The assets\blockstates folder
blockstates_pathlet = "blockstates"
# The assets\lang folder
lang_pathlet = "lang"
lang_en_US_pathlet = path.join(lang_pathlet, "en_US.json")
# The assets\models folder
models_pathlet = "models"
mdl_block_pathlet = path.join(models_pathlet, "block")
mdl_item_pathlet = path.join(models_pathlet, "item")
# The assets\textures folder
textures_pathlet = "textures"
txtr_blocks_pathlet = path.join(textures_pathlet, "block")
txtr_items_pathlet = path.join(textures_pathlet, "items")
txtr_entities_pathlet = path.join(textures_pathlet, "entity")

# The main\resources\data folder
data_path = path.join(resources_path, r"data")
# Final paths.
recipes_pathlet = "recipes"
loot_tables_pathlet = "loot_tables"
loot_blocks_pathlet = path.join(loot_tables_pathlet, "blocks")
loot_entities_pathlet = "entities"


# Own Mod Graphics folder
new_graphics_folder = r"C:\Users\Julio Hong\Desktop\Minecraft Stuffcraft\Own Mod Graphics\Warehouse_Exhibition"
# Expected .png name?

# Can capitalise for the en_US lang
dye_colours = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
               'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black']
dye_colours_CN = ['白色', '橙色', '品红色', '淡蓝色', '黄色', '黄绿色', '粉红色', '灰色',
                  '淡灰色', '青色', '紫色', '蓝色', '棕色', '绿色', '红色', '黑色']
# Temporary list to remind myself of the object types
object_types_all = ['slime_block', 'slime_ball', 'slime_entity']


# All functions
# ========================================
def text_guide_singular():
    print("Please input the parameters in this format:")
    print("add_block(cased_output_modid, cased_object_name)")
    # Include available pathlets
    print(assets_path)
    print(lang_pathlet)
    print(blockstates_pathlet)
    print(mdl_block_pathlet)
    print(mdl_item_pathlet)
    print("")
    print(data_path)
    print(loot_blocks_pathlet)
    print(loot_entities_pathlet)

text_guide_singular()


# Block object requires 4 JSONs: BlockState, Model/Block, Model/Item, LootTable/Block
def add_block(cased_output_modid, cased_object_name):
    # Set to lowercase for paths.
    output_modid = cased_output_modid.lower()
    object_name = cased_object_name.lower()
    # BlockState
    modify_template_from_input(output_modid, 'assets', blockstates_pathlet, object_name)
    # Model/Block
    modify_template_from_input(output_modid, 'assets', mdl_block_pathlet, object_name)
    # Model/Item
    modify_template_from_input(output_modid, 'assets', mdl_item_pathlet, object_name, "placeholder_blockitem.json")
    # LootTable/Block
    modify_template_from_input(output_modid, 'data', loot_blocks_pathlet, object_name)
    # Add lang entry using another function.
    output_lang_file = path.join(output_path, assets_path, output_modid, lang_en_US_pathlet)
    append_lower_upper_to_json(output_modid, output_lang_file, 'Template_block', cased_object_name)


# A function that takes in a path, modid and object name to create an appropriately-pathed JSON based on a template.
# I'm actually missing the typing restrictions of Java. What are these variables supposed to be?
# Replaces existing JSONs if already present. Less risky with some form of version control available.
def modify_template_from_input(output_modid, assets_or_data, final_path, object_name, placeholder="placeholder.json"):
    # template_path, resources_path and template_modid are global variables.
    # Choose between assets_path or data_path.
    if assets_or_data == "assets":
        template_json = path.join(template_path, assets_path, template_modid, final_path, placeholder)
        specific_output_path = path.join(output_path, assets_path, output_modid, final_path)
    elif assets_or_data == "data":
        template_json = path.join(template_path, data_path, template_modid, final_path, placeholder)
        specific_output_path = path.join(output_path, data_path, output_modid, final_path)
    # Creates the output directories and subdirectories if they don't already exist.
    pathlib.Path(specific_output_path).mkdir(parents=True, exist_ok=True)
    # Create the output JSON.
    output_json = path.join(specific_output_path, object_name + ".json")
    # If output JSON already exists (maybe from previous attempts), then delete. Overall effect is replacement.
    try:
        remove(output_json)
    except OSError:
        pass

    with open(template_json, 'r+') as f:
        # Load JSON as Python object
        data = json.load(f)
        # Convert to string for string manipulation.
        input_str_json = json.dumps(data)

        # Replace all mentions of 'modid' with output_modid.
        output_str_json = input_str_json.replace('modid', output_modid)
        # Replace all mentions of 'template' or variants with object_name.
        # Check for variants first, then finally template.
        text_checks = ["template_block", "template_item", "template_entity", "template"]
        for check in text_checks:
            if check in output_str_json:
                output_str_json = output_str_json.replace(check, object_name)

        # Convert to JSON.
        output_data = json.loads(output_str_json)
        # Opens file for reading and writing. File is created if it did not already exist.
        handle_output_json(input_json=f, output_json=output_json, output_data=output_data)


# Replaces paths and translations in en_US.json.
def append_lower_upper_to_json(output_modid, input_json_path, cased_template_string, cased_output_string):
    template_string = cased_template_string.lower()
    output_string = cased_output_string.lower()
    output_json_path = input_json_path
    # Generates a new entry
    # Check if the namespace is an advancemeent or not.
    namespace = template_string.split('_')[1]
    if namespace == 'advancements':
        output_key = namespace + '.' + output_modid + '.root.' + output_string
    else:
        output_key = namespace + '.' + output_modid + '.' + output_string

    with open(input_json_path, 'r+') as f:
        # Load JSON as Python object
        data = json.load(f)
        # Convert to string for string manipulation.
        input_str_json = json.dumps(data)

        # Don't replace. Append a new key-value pair after the template entry.
        input_list_json = input_str_json.split(cased_template_string)
        input_list_json.insert(1, cased_template_string + '", "' + output_key + '": "' + cased_output_string)
        output_str_json = ''.join(input_list_json)

        # Convert to JSON.
        output_data = json.loads(output_str_json)
        # If output JSON already exists (maybe from previous attempts), then delete. Overall effect is replacement.
        f.close()
        try:
            remove(input_json_path)
        except OSError:
            pass

        # Opens file for reading and writing. File is created if it did not already exist.
        handle_output_json(input_json=f, output_json=output_json_path, output_data=output_data)


def handle_output_json(input_json, output_json, output_data):
    g = open(output_json, 'a+')
    g.seek(0)
    json.dump(output_data, g, indent=2, separators=(',', ':'))
    g.close()
    input_json.close()
    try:
        input_json.close()
    except FileNotFoundError:
        pass


# Renames modid in the default en_US.json.
def rename_lang_file(cased_output_modid):
    # Set to lowercase for paths.
    output_modid = cased_output_modid.lower()
    template_lang_file = path.join(template_path, assets_path, template_modid, lang_en_US_pathlet)
    output_lang_file = path.join(output_path, assets_path, output_modid, lang_en_US_pathlet)
    # If output JSON already exists (maybe from previous attempts), then delete. Overall effect is replacement.
    try:
        remove(output_lang_file)
    except OSError:
        pass

    with open(template_lang_file, 'r+') as f:
        # Load JSON as Python object
        data = json.load(f)
        # Convert to string for string manipulation.
        input_str_json = json.dumps(data)
        # Replace all mentions of 'modid' with output_modid.
        output_str_json = input_str_json.replace('modid', output_modid)
        output_str_json = output_str_json.replace('Translated_MODID', cased_output_modid)
        # Convert to JSON.
        output_data = json.loads(output_str_json)
        # Opens file for reading and writing. File is created if it did not already exist.
        handle_output_json(input_json=f, output_json=output_lang_file, output_data=output_data)










# A function to generate the object name based on all available colours
def generate_dyed_objects(object_type, dye_colours, suffix=''):
    # Might want to add a check to determine if the colours goes in front or behind
    dyed_list = [object_type + '_' + dye for dye in dye_colours]
    if suffix == '':
        return dyed_list
    else:
        suffix = '_' + suffix
        return [dyed_object + suffix for dyed_object in dyed_list]


# A function to transfer PNG files from the working folder to the target folder
# Works for single object or a list
def transfer_png_to_assets(source_path, item_block_entity, dyed_object_single_or_list):
    missing_obj = []
    if item_block_entity == 'item':
        target_path = txtr_items_path
    # For blocks, this is to transfer the BlockItem texture
    elif item_block_entity == 'block':
        target_path = txtr_blocks_path
    elif item_block_entity == 'entity':
        target_path = txtr_entities_path
    else:
        return 'Invalid object type inputted. Please try again.'

    def single_transfer_png(source_path, target_path, obj, missing_obj):
        source_file = path.join(source_path, obj + '.png')
        target_file = path.join(target_path, obj + '.png')
        # print(source_file)
        if path.isfile(source_file):
            move(source_file, target_file)
        else:
            missing_obj.append(obj)
        return missing_obj

    # Check if file exists in source_path
    if type(dyed_object_single_or_list) != list:
        missing_obj = single_transfer_png(source_path, target_path, dyed_object_single_or_list, missing_obj)

    elif type(dyed_object_single_or_list) == list:
        for obj in dyed_object_single_or_list:
            missing_obj = single_transfer_png(source_path, target_path, obj, missing_obj)

    if missing_obj:
        print(str(missing_obj) + ' images')


# The basic function to create JSON files linked to a list of dyed objects.
def create_json_to_target(template_json_path, target_path, dyed_object_single_or_list, json_input):
    missing_obj = []
    data = 0


    # Changes the JSON and saves it
    def single_create_json(template_json, obj, json_input, specific_namespace):
        # specific_namespace = ns_list.copy()
        # # Read the file
        # f = open(path.join(template_json))
        # # Open the template JSON
        # data = json.load(f)

        # Read the template JSON
        # Only r+ can both read and write
        with open(template_json, 'r+') as f:
            # Create the output path
            output_json = path.join(target_path, obj + '.json')
            # Load JSON as Python object
            data = json.load(f)
            # print('data is ' + str(data))
            # print('ns_list is ' + str(specific_namespace))

            # Edit the input fields
            # If ns_list[0] is a single entry in the case of Block Model.
            if type(specific_namespace[0]) != list:
                for entry in specific_namespace[1]:
                    data[specific_namespace[0]][entry] = json_input

                # May have to edit this data format separately
                g = open(output_json, 'a+')
                # data = CompactJSONEncoder().encode(data)
                g.seek(0)
                json.dump(data, g, indent=2, separators=(',', ':'))
                # json.dump(data, g, indent=2, separators=(',', ':'), cls=CompactJSONEncoder)
                f.close()
                g.close()

            # Or if it's a list, recursively declare a variable to get to the input field within these nested dicts/lists.
            elif type(specific_namespace[0]) == list:
                pointer = data
                # Keep moving down a nested layer
                while len(specific_namespace[0]) > 1:
                    # print(specific_namespace[0])
                    pointer = pointer[specific_namespace[0][0]]
                    specific_namespace[0].pop(0)
            # The most nested value is reached
                pointer[specific_namespace[0][0]] = json_input
            # print(pointer)
            # print(data)

            # # Write to output file
            # # Only r+ can both read and write
            # data['pools'][0]['entries'][0]['name'] = 'ohno'
            # # a+ to create file if it doesn't already exist
            # # Might want to add in a check for exists()
            # g = open(path.join(loot_blocks_path, 'slime_block_black.json'), 'a+')

            # a+ to create file if it doesn't already exist
            # Might want to add in a check for exists()
            g = open(output_json, 'a+')
            g.seek(0)
            json.dump(data, g, indent=2, separators=(',', ':'))
            f.close()
            g.close()

            return data

    # Provide template JSON, and input field.
    # Or might be easier to just create different JSON formats based on target_path

    # Determine json_input based on target_path
    # Model for Block. Input fields: 'particle', 'texture'
    # ns_list will contain the hierarchy of folders.
    # Each entry is an input field. Nested list is a hierarchy.
    # Do I put this check into this function or outside of it?
    # Loot Table. Input field: 'pools': [{'entries': [{'name'}]}]
    if target_path == loot_blocks_path:
        ns_list = [['pools', 0, 'entries', 0, 'name']]
    # Loot Table for entities is actually almost the same as loot table for blocks.
    # Just need to debug first, but it worked when I substituted loot_blocks_path.
    # OK wait, the filename is different from the changed field. That's the probelm.
    # Blockstate. Input field: 'variants': {'': {'model'}}
    elif target_path == blockstates_path:
        ns_list = [['variants', '', 'model']]
    # Model for Item or BlockItem. Input field: 'parent'
    elif target_path == mdl_item_path:
        ns_list = [['parent']]
    # Model for Block.
    # Was there something wrong with this? I can't recall.
    elif target_path == mdl_block_path:
        ns_list = ['textures', ['particle', 'texture']]
        # Just make copies that are named appropriately.
        # Don't need json_input for now.
    else:
        return 'target_path is not supported'

    if type(dyed_object_single_or_list) == list:
        for obj in dyed_object_single_or_list:
            if target_path == mdl_block_path:
                output_json = path.join(target_path, obj + '.json')
                copy(src=template_json_path, dst=output_json)
            else:
                specific_input = json_input + obj
                specific_namespace = deepcopy(ns_list)
                data = single_create_json(template_json_path, obj, specific_input, specific_namespace)

    # Assume single entry
    else:
        if target_path == mdl_block_path:
            output_json = path.join(target_path, dyed_object_single_or_list + '.json')
            copy(src=template_json_path, dst=output_json)
        else:
            data = single_create_json(template_json_path, dyed_object_single_or_list, json_input, ns_list)

    # return missing_obj
    return data


def transfer_block_jsons(toggle_list, template_dict, source_path, dyed_block_list, lang_seed, need_recipe=False):
    # Need a way to toggle which JSONs to output.
    # Maybe some require more customisation so there's no point to output them.
    # So put placeholder values for unused params, then follow the toggle_list.
    # Example: '111101' to avoid recipes

    # This would work for adding lists of dyed blocks with simple behaviour.
    missing_jsons_dict = {'model': None, 'blockstate': None, 'loot_table': None, 'recipe': None}

    # Since the input is a list, use list iteration.
    # Use a list length of 1 for single objects.
    # for object in dyed_block_list:

    if toggle_list[0] == '1':
        # Loot Table. Input field: 'pools': [{'entries': [{'name'}]}]
        # DONE
        create_json_to_target(template_json, loot_blocks_path, dyed_block_list, json_input)

    if toggle_list[1] == '1':
        # Blockstate. Input field: 'variants': {'': {'model'}}
        # DONE
        create_json_to_target(template_json, blockstates_path, dyed_block_list, json_input)

    if toggle_list[2] == '1':
        # Model for BlockItem. Input field: 'parent'
        # DONE
        create_json_to_target(template_json, mdl_item_path, dyed_block_list, json_input)

    if toggle_list[3] == '1':
        # Model for Block. Input fields: 'particle', 'texture'
        # Just copy and rename JSONs
        # DONE
        create_json_to_target(template_json, mdl_block_path, dyed_block_list, json_input)

    if toggle_list[4] == '1':
        # Recipe, if needed. Input field (for ColouredSlimeBlocks): 'result'
        # Requires a template recipe
        # Problem: What about the ingredients?
        # DONE, but add recipes outside of this function
        recipes_path

    if toggle_list[5] == '1':
        # Add to lang (needs its own function)
        # DONE
        translate_to_lang(object, obj_type, lang_seed, language='en_US')

    # Put lists of added objects together, so at least can move them together too.

    return missing_jsons_dict



# Input object_type, dye_colours and translation template to get translations for all.
# def translate_to_lang_en(lang_json, namespace_obj, obj_translation):
#     lang_json[namespace_obj] = obj_translation


def translate_to_lang(item_block_entity, obj_type, lang_seed, language='en_US'):
    lang_json = path.join(lang_path, language + '.json')
    prefix = obj_type + '.' + mod_id + '.'

    with open(lang_json, 'r+') as f:
        lang_data = json.load(f)
        # Single object
        if type(item_block_entity) != list:
            obj_translation = lang_seed
            lang_data[prefix + item_block_entity] = obj_translation

        # A list of objects
        else:
            for obj in item_block_entity:
                if 'light' in obj:
                    colour = 'Light ' + obj.split('_')[-1].capitalize()
                else:
                    colour = obj.split('_')[-1].capitalize()
                obj_translation = colour + ' ' + lang_seed
                lang_data[prefix + obj] = obj_translation

        # Returns cursor to start of JSON file, and allows existing data to be overwritten
        f.seek(0)
        json.dump(lang_data, f, indent=2, separators=(',', ':'))
        f.close()


# Input recipe ingredient, assuming recipe is a Python JSON object for shaped recipes.
def design_recipe_ingredient_shaped(template_recipe, ingredient, key_of_ingred):
    template_recipe['key'][key_of_ingred]['item'] = ingredient
    return template_recipe


# Input recipe ingredient, assuming recipe is a Python JSON object for shapeless recipes.
def design_recipe_ingredient_shapeless(template_recipe, ingredient):
    template_recipe['ingredients'][0]['item'] = ingredient
    return template_recipe


# Input recipe product.
def design_recipe_product(template_recipe, product, count_of_prod=1):
    template_recipe['result']['item'] = product
    template_recipe['result']['count'] = count_of_prod
    return template_recipe


# Change the entire recipe based on ingredients
# Product is required for output_json
# Check if there are any ingredients or products too.
# Only works for minecraft:crafting_shaped.
def design_new_recipe(mod_id, crafting_type, template_product, ingredient='',  product='product', key_of_ingred='', count_of_prod=1, name_of_recipe='none'):
    if name_of_recipe != 'none':
        template_json = path.join(recipes_path, template_product + '.json')
    else:
        # Apparently recipe name doesn't have to be the product.
        template_json = path.join(recipes_path, name_of_recipe + '.json')

    with open(template_json, 'r+') as f:
        # Create the output path
        # output_json = path.join(recipes_path, product.split(':')[1] + '.json')
        output_json = path.join(recipes_path, product + '.json')
        ingredient = mod_id + ':' + ingredient
        product = mod_id + ':' + product
        # Load JSON as Python object
        data = json.load(f)
        if ingredient:
            if crafting_type == 'crafting_shaped':
                data = design_recipe_ingredient_shaped(data, ingredient, key_of_ingred)
            elif crafting_type == 'crafting_shapeless':
                data = design_recipe_ingredient_shapeless(data, ingredient)
        if product != 'product':
            data = design_recipe_product(data, product, count_of_prod)

        g = open(output_json, 'a+')
        g.seek(0)
        json.dump(data, g, indent=2, separators=(',', ':'))
        # json.dump(data, g)
        f.close()
        g.close()


def design_multiple_recipes(mod_id, crafting_type, template_product, ingred_list=[],  prod_list=[], key_of_ingred='', count_of_prod=1, name_of_recipe=''):
    if len(ingred_list) != len(prod_list):
        return 'Mismatch between number of ingredients and number of products'
    else:
        for i in range(len(ingred_list)):
            design_new_recipe(mod_id, crafting_type, template_product, ingred_list[i],  prod_list[i], key_of_ingred, count_of_prod,
                           name_of_recipe)


def check_block_textures(block_sides=[all]):
    # Alternate sides inputs: [bottom, side, top/platform] for cactus/pistons
    # [end, side] for logs
    # [particle, pattern] for glazed terracotta
    return None


def generate_all_dyed_objects(object_types_all, dye_colours):
    # dyed_obj_lists = []
    # for obj_type in object_types_all:
    #     dyed_obj_lists.append(generate_dyed_objects(obj_type, dye_colours))

    dyed_obj_dict = dict.fromkeys(object_types_all)
    for obj_type in object_types_all:
        dyed_obj_dict[obj_type] = generate_dyed_objects(obj_type, dye_colours)

    return dyed_obj_dict

def transfer_all_generated_files(source_path, target_path, object_types_all):
    # Initialise the list of lists - dyed_obj_lists
    dyed_obj_lists = generate_all_dyed_objects(object_types_all, dye_colours)

    # for obj_type in object_types_all:
        # Add textures
        # For blocks specifically, need to add the textures
        # How to check if the object_type is a block?
    return None

# Might need a function to generate filepaths e.g. for SlimeRenderer to find textures for each Coloured Slime


# https://stackoverflow.com/questions/16264515/json-dumps-custom-formatting
# Author: Tim Ludwinski, adapted by jmm
class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small lists on single lines."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""

        if isinstance(o, (list, tuple)):
            if self._is_single_line_list(o):
                return "[" + ", ".join(json.dumps(el) for el in o) + "]"
            else:
                self.indentation_level += 1
                output = [self.indent_str + self.encode(el) for el in o]
                self.indentation_level -= 1
                return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"

        elif isinstance(o, dict):
            self.indentation_level += 1
            output = [self.indent_str + f"{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()]
            self.indentation_level -= 1
            return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"

        else:
            return json.dumps(o)

    def _is_single_line_list(self, o):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, (list, tuple, dict)) for el in o)\
                   and len(o) <= 2\
                   and len(str(o)) - 2 <= 60

    @property
    def indent_str(self) -> str:
        return " " * self.indentation_level * self.indent



# They see me walkin', they hatin'
#                                                                             .
#                                                                          ,..,.&
#                                                                         ,( .....,
#                                                                        *..(&**#.
#                                                                       /..//,@(
#                                                                      (.*&&#%,#(#&#&*
#                                                                  *@/,,,,,,*@&&%@&*...,,%/                          (%&%#*...,(%&@#*
#                                                              ,#...%@@@@@@@@@@@@@@@@@@@@@@&        .%&@&@@@@@@#/**(&&@&@@@@@(#*. .&
#                                                           ,,..@%.,,.... *@(.,.......**#&@@@%/.&&.,#%&%(,((.&@@@@@@@@@@@@@@@@@@.,#
#                                                          /.#%......#(@@&.....,.,.........,.,...,#@@,,,,#.%@./@/@@@@@@@@@@@@@@%,&
#                                                        .%(....//..,..,(@@@.@....... ,((/.......*#%*@&@(....,%&,#,@@@@@@@@@@@@(**
#                                                      &(......,...*/@(..&&@.*,,.............,//##(#,...(&&@@@@&..%,,@@@@@@@@@@**%
#                                                   .@.,(%#(,..*(,##@,,@#../.#/*#%%%&@@@#/..,###**/.,...,#@,,..,//&@@..@@@@@@@@%./
#                                                 &.......,....#&(%/@.@@@#&.,.(&&@(/#/(%#/, ,..(&@#%##%,(,..##*%/,.,@%../@@@@@@@..%
#                                             .*,......,....(#,.%/@%,@@....,.*%...,,.#,@@@@@@@%#%,*%&&,(@@.,*.....,% .....@@@@@@&..
#                                          (.......,.....#&(.. .,/@@,@@@/..,,...,/. ,#,#@&.&@&@@@&,/# # %.%./#/............%@@@@@,.%
#                                      ,(.......,(&(,.,//(@%%(@/@(.@(#.@*...,......../.,@@(@@,,@@#,*/%&@/#.&(@/#.(#........,(@@@@@,.
#                                   (...,..*..(#%(((/(,(#&@@@#@@(%......,,..,........**@@(%@@.#@@*.,.%/*,(**.(,#.,(/....... .(@@@@ .(
#                               (%@*..*(,.,........*%%@@. */@@/@&#@&@...(%............@@//@@./@@@./,...,.,,,(#.*#*,...........@@@@ .%
#                          *.@@%&@@*......,*#(@&#@@@&          /%%((,*&@&,.%&&&...,...@@#@@,/@@@&/#.........#&#,*#*,..........@@@(.*,
#                         #.@@@/%@@&,..*#*(@..,.(&                       ,@&@,.@&..,/(@@@@.@@@@@@........,.,#/(/,( ........,.@@@&, .
#                         /.@@@/*@@@.#**(%@&@@/                              .&,.,.%@@@@*#@@@@*........,....,*. ,....,.....,@@@//,
#                        #..@@@@#/(%(##,&.#@,                                    . @@(%%@@@#........,..,/&,.......,.,......@@#/.#
#                       /&,,(@@@@@@@@@@@@(@@                        .            #@(%@@@#,......,/&#,/.*//,,.,..,.......,@@&(*#
#                      @..*@%..*(/###(/@&                           @@,        /@&@@@/(.,,.(&##@,,%#*( &.#............&&&@&
#                    &,..,..*,((((**(/##&/                          &@@@@#   #@@@@%%,...#.*,..*##&#.*/#.,.........///#,/(&%*@,
#                  (.,#,....(//@&(%&/,.,..*.                        .@@@@@@@..,.(@.*..&*,(,(/./%#%,,**....,,........,.&,.,@@.&&.
#                /..*##(@@@@&@@@@@@@&@%#@&/#                     #@@@@@@@@@@@@@@&*..%//.%%,.*..%@.....,,,....**.....,@..*%@./@/..*,
#              ,...,  ,*#@, ,@&&@@@#   & ,.                   @@@@@@@@@@@@@@@@@@@(#@&#..,.#&*,%,(#...,.,#,......(.(,@#(*,(,* ..,,,...(.
#               ,%@   &,##  ...%,&&@                       /          %@@@@@@@@@@@@,/*#%*@.@#.(#@.....,*..@%@@&.&/@@@@.,......,,..,...##*@
#               ..%   #/@%  ,#&@ %%@                                 /@@&(@@@@@.(.%,,*,#/%,&..**....((....,.,,./@,% (*#%,(/*((#/*(.......,.,,&#.
#               ##    . .*   ..(                                   *#@@@@@(...,,,,.#@*,#(#,%./....,....,(.,......,@(..,,*..,,.......,//##@&////(@&
#                      #.(   #%                                       ..(/&*.#,(..#.**./#.*/&,...#..,(..,.........#@    /@&/(*#(#(((%(&&%%#(,....(%@
#                                                                    &*.#%*(..&.....,@@//...#,,#....(..*...........,@          ,&&##(//**,.#,(%,.....&
#                                                                      @%...&&.......,(....,.... ,,.//.......,.......@%               #*#(.............%
#                                                                      /@*/%/(..... #...................*(%%%#%%(((((.%@/                 @%#..,.....#,.,(
#                                                                       ,@%*(.....(...,,......*%%(. ..,#@@@@@@@@@@@&/**..#%                %&&@%@( ......,./
#                                                                       ,%/&,...*...,..,,./.....(@@@((/ %(/,*/@@@@@@@@@,&*                    &/%(**/,....@,@(
#                                                                        %@%,..*...,,(*((...&@%(#&*(#,#(&#*(.@@@@@@@&#(                          #////,...,,#*.(
#                                                                        #&@,%,,*#.#/*#..(@##(,##.%(///#,/(*#%@@@&*&                               #((**...(%&..@@
#                                                                        .&/%/@%/(%,#..#@,##,/,......,.,..,,,%@%%.                                   /(,...,*..&@@&@@#
#                                                                         &&@#,%(/,..%@/#..................,(&%(                                       /@##&@@@@@..@@@./
#                                                                         (@#,%*%*.%@.,........... ........../&@&                                        .@&/.../@@@&.%&       #
#                                                                         &**/#/,*@,........ ................ ..,&(*((                                     ,@@@@@@..*@@@@./.  ..,  ,*
#                                                                        ,&#*,.,@(,,...................,.........&.,#&%(                                     (...(&%..,..,@(#(&@@*%**.#
#                                                                       .%%(..&@*..,.........,...**#.........*,.,/(,,#(,##                                       ,/*.,......,.,.,(#/@.%
#                                                                     .#*...*@@@*.,*/...........*#......./#...,#,..*#@@@#.&                                         #/(/#,..& ..*@@&#,#
#                                                                      .(##%#&@@&........,.,..,(*..../(,*,&*..%@@%##%.,.,#(                                           .@,,,#%@@/#&,%
#                                                                               #............,%.*&,...,(#.,@(.....,. ....../                                             *%/..*/..*&*
#                                                                            .#,(/ ......,,&@&&&%..#.(%@@/(..,@..,...........&
#                                                                            @,,...(#,&,.(#,(@#& ,&&*@........,.*@//.....,...*@
#                                                                     .(@@@@%@@/,,, *%.&/@.&%%&&@@&,#.........,....,*&.......%@@%#
#                                                                  /@.,.,*,/*..,*&&.,/&%#*(&%#@@%. ... .............,/,(%...#/@@@#@
#                                                                   @(#%&&%(*/#&&(.%*%((%%,#@%/,//......................@.#@@@@@,*.
#                                                                   .@@@@#@/,....,%@@/,(@%.%*(/%%%%(*/**//((/(/*,.........,&@#@@.
#                                                                    @@@#@#.%%#*,&#/(#(&@@#,%%#..,........,.,...,,..........,,(/
#                                                                  .&&&%(&#..,,,*@@/.&(&(,,(,%&%(&#,@*,............,........,.@%.%,
#                                                                  &%(..,,@&&%,....../@@&@@#&#*.,.(@*%##,((.,,...,,........,.*&@,,@.
#                                                              .&(,#.*@&@#%((&/%/,. ,....%@%@@@@*&#.,../,&%//#,.,....,...,.%.,..*@#
#                                                            ((&&(/&%#(*,,/&@##/#.,#&&(%@@**.*/,.#@@%&.,,..,...,,((&@@@%,,..,,/%(&&
#                                                         *&#@#%&#((/#((,...........*.,#%%@*##,#@/&@&,/@(....,,...../(/*,,......*..*(
#                                                       &&(&#&(*.....,,........,**#&(,...&@&(&@@%,/&(%*((..*&,........,.,,..(#%&@@@%
#                                                    (//,..........,...,..*&%,.,.,@%,,&@@@@%@&/   %#/#%%*##...,.*%.....,........,##.#
#                                                  #*..,......,../&(,...,,.,..//,....,&*            #,/%@#/(...,.....,#,,.,..,...,.(/*
#                                               @/...(...*&, ,..,..,,.,&%(( ...,...&                  #%(%#&,...........,..,........##(
#                                            ,(,...,.....,.....,##.,,,.,#.....,&.                       /#@//,(....,.,.....,..,.......//
#                                          %.,..,....,....//....,..(*.,.../((                             ,(%,.....,..,...,............,(
#                                        @@/...,......,.,(#(/##&*.....(#&                                   .@&//,.......,.......,.......#
#                                      &%........,.(,@....,,..,,%%@@@*                                         @%.,................,......%
#                                     %@*..,*%%....#,&@%..&,.#@@@&                                               &#%*.......,,..,.........(@
#                                     @@@@@@,......#..&&#,(@@,(                                                    &&@,...........,........@@
#                                     @@@&,...,. ,.#..(%&..@,                                                        #//................,../@@.
#                                    *@@/,......,..%(,,&@@/                                                            ,&.........,,,..,,,,(&%%,*&
#                                    @&,,.,......,..%,,#,                                                                 @..............,(/(@&@.@
#                                   #@*..*,....,....*@,.,,                                                                  %............../%%(.*@*.,&@,
#                                   @@,.,.....,.,..,,@@@                                                                      *(.,.......(/&%,.%@...*%#*.(%(,
#                                  (,#,.*..........,.@.                                                                         .#......,,*,.,,#.,.,*,,.........,#/
#                                 %.(,.(.. ..........*/                                                                            &/.........,&*,....,............,,.*&.
#                                ,,*.,.,.........,..,#*                                                                              #,.(@@@@@@@.#%..,......,.,..,.,.,...,.,,#(
#                                &%. /#....,. ......*@                                                                                    @@@@*.,&@@@,,.......,.....,,,.,., ...,.*@@%.(
#                               *#(..#,,.........../@                                                                                          &@@/,,&@@@@&#(......,.....,.,....,,#@@*,(
#                              ,/(,,.&......,....*#@.                                                                                              .&%.*(*..*(&@&(&%((/(*//(/(((#((%&(/*.
#                              /**,,.(...,...,,.,@@%                                                                                                    ((,,(%#(#%%(*...,*#@%(///(###(((%
#                             &((%..%.....,..,(*,*@                                                                                                         .&/(*,**#(/((*,/%#&(.,...,,**/((//#
#                            **//...&....,.,.,#,.,(                                                                                                              ((#/(#*.,//,.......,../@&...(@@...,#
#                            (#*((,%@..,..,(%..,.,                                                                                                                   */(* ./#(....,.,,.,%,@@@@@@*,....,
#                           &,,/,..@#... /.(.....#                                                                                                                       ((./(/,,.....(@@,@@@@@@@@@(..(
#                          #.((&.,*@%.../(..,...,&                                                                                                                           %,.,.,@@@@@@/(@@@@@@@@%..#.
#                         *..,,/.,*(&,./.(,......@                                                                                                                           (/@@@@@&.%..%@@@@@@@@@,,.(
#                        .(./#%../#(%../#(....,.,@                                                                                                                           //@@%..@#(..@@@@@@@@@,,%%(
#                        &./,,*..%@.#..%(,....../@                                                                                                                           /./&@@@@@(#/@@@@@@@@%(@
#                       &*,#(,...&(/#,.(&(#....*#@                                                                                                                              /@@@@@@@&&*/@*@@@#(
#                      @,(*/#(../( /%..#(*,.,.%#@(,.                                                                                                                            #.###,//##@%,,@@@#..#
#                    (%.,/&(@,..&&#*/. (*..%//@/.#                                                                                                                            //,%(,(#*&@@@@@%@@@(..&
#                   (%..*(&%**,#.&(,#,,,*(%@*#.%                                                                                                                                 &(#  #&@@@@@@@@@#..%
#                 %(/.,.@%(##..%#,((#...&%&%.(                                                                                                                                ,/      #///*,%@@@@#..%
#              ,(/(*...,%*//..%.&.##%..(,..*                                                                                                                                  /#      *%%/%%@@@@@..%
#                ,&(...#,(/,#*(,**(%%/.,.,,                                                                                                                                           *@@@@@@@@@%..#
#                    @@*#*,*/,.(.(/(#..,,                                                                                                                                             (,.&@@@@.,..#
#                     ,@.**/,,,&./(,..@                                                                                                                                               @@@&.,....*#
#                      @((//..,#,..,@#                                                                                                                                                 *.......%/
#                      /&//*...&.@@./                                                                                                                                                    #,,//
#                      *@(*/,.,@&,%%
#                     @..&((,.*@.(%.
#                 . &@,, ..,@,.@*&@.&
#             (..@@/@%.....,,,,#@@*&&
#            %(.#@/@@....,. /,@@.(,@&
#            #.&*,........(,.%@@@@@@@.
#            .,/%@&@@@@@&@@&*@@@@@@@&.,
#         //,, *%@@@@@@@@&@@@@@@@@@(.,,,
#        *#  (,&,@@@&%/,/&@@@@@@@@@.,..%
#        #..(&@/%#,(%/#@@%@(@@@@@@&.,.,,
#          (@##@@&##&,@@@#@.&@@@&..,..%
#         (/%&@@@&%.(@@&@@@@@##(%(%/
#     ,/&,#%&@@@@#%/@@#@@@@*(
#       @@@@@@@@&.#@&@@@@@.*
#     &@@@@@@@@@@@@@@@@@#,/
#   (.,,,,(@@@@@@@@@@@#..(
#  #.,,,.,,,(@@@@@@%.*##
# *.,...,.,&@@@@,..%%
#  %....,..,,.,.,,#
#     &@@@#/,(#,