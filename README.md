# Helper-Scripts-Laplio
Small scripts to streamline the workflow of mod-making in Fabric. Written in Python for now.

## Description of each script (in order of use frequency):
- java_code_replace: Takes a single input of code/JSON and generates multiple copies that differ only in the variable name. Used mostly for Coloured Slimes at this point.
- biome_sec_swapper: Swaps a dict of Biome:ColouredSlime to create a dict of ColouredSlime:Biome
- string_to_list: Converts a string of elements into a list. "elm_01, elm_02, ..." -> ["elm_01", "elm_02", ...]
- fabric_json_creator: Ambitious script that would automatically generate all the JSONs associated with adding a block or item into the appropriate folders of a Minecraft mod. Still WIP.
