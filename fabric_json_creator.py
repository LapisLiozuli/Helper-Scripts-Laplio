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
from os import path, remove, rename
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
# output_path = r"C:\Users\Julio Hong\Documents\LapisLiozuli\testcopy"
# test_path = r"C:\Users\Julio Hong\Documents\LapisLiozuli\test-copy"
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
lang_en_us_pathlet = path.join(lang_pathlet, "en_us.json")
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

# Can capitalise for the en_us lang
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
    output_lang_file = path.join(output_path, assets_path, output_modid, lang_en_us_pathlet)
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


# Replaces paths and translations in en_us.json.
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


# Renames modid in the default en_us.json.
def rename_lang_file(cased_output_modid):
    # Set to lowercase for paths.
    output_modid = cased_output_modid.lower()
    template_lang_file = path.join(template_path, assets_path, template_modid, lang_en_us_pathlet)
    output_lang_file = path.join(output_path, assets_path, output_modid, lang_en_us_pathlet)
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


def mod_renamer(output_repo_path, cased_new_modid):
    # Create a list of filepaths for both template and output.
    author_path = r'src\main\java\com\lapisliozuli'
    new_modid = cased_new_modid.lower()


    def create_paths(repo_path, repo_modid):
        # Renaming file content only
        # fabric.mod.json
        fabric_mod_json = path.join(repo_path, resources_path, 'fabric.mod.json')
        # gradle.properties
        gradle_properties = path.join(repo_path, 'gradle.properties')
        # en_us.json
        en_us_json = path.join(repo_path, assets_path, repo_modid, lang_en_us_pathlet)
        # README.md
        readme_md = path.join(repo_path, 'README.md')

        # Renaming files
        # modid.mixins.json
        mixins_json = path.join(repo_path, resources_path, 'modid.mixins.json')
        # ExampleMod
        initialiser = path.join(repo_path, author_path, repo_modid, 'ExampleMod.java')
        # ExampleModClient
        initialiser_client = path.join(repo_path, author_path, repo_modid, 'ExampleModClient.java')

        return [fabric_mod_json, gradle_properties, en_us_json, readme_md, mixins_json, initialiser, initialiser_client]

    template_paths = create_paths(template_path, template_modid)
    output_paths = create_paths(output_repo_path, new_modid)

    # Need to rename folders first. Might need intermediate paths.
    rename(path.join(output_repo_path, author_path, template_modid), path.join(output_repo_path, author_path, new_modid))
    rename(path.join(output_repo_path, assets_path, template_modid), path.join(output_repo_path, assets_path, new_modid))
    rename(path.join(output_repo_path, data_path, template_modid), path.join(output_repo_path, data_path, new_modid))

    # Traverse the filepaths to replace content and save in output repo.
    # Currently this dupes code rather than replacing.
    for i in range(len(template_paths)):
        with open(template_paths[i], 'r') as fin:
            filedata = fin.read()
            filedata = filedata.replace('modid', new_modid)
            filedata = filedata.replace('ExampleMod', cased_new_modid)
        with open(output_paths[i], 'a+') as fout:
            fout.write(filedata)
        fin.close()
        fout.close()

    # Then traverse some of the files to replace the name.
    # Create copy of new file with new filename, then delete old copy.
    rename(output_paths[4], path.join(output_repo_path, resources_path, new_modid + '.mixins.json'))
    rename(output_paths[5], path.join(output_repo_path, author_path, new_modid, cased_new_modid + '.java'))
    rename(output_paths[6], path.join(output_repo_path, author_path, new_modid, cased_new_modid + 'Client.java'))


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