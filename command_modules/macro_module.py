import os
import json
import re
import readline
from config import MACRO_DIR
from commands import process_command

if not os.path.exists(MACRO_DIR):
    os.makedirs(MACRO_DIR)

def create_macro(content):
    """
    Create a macro from a string with the following format:
      "<command1>; <command2>; ...; <commandN> save as <macro name>"
    
    • Each <command> must be a valid token command (e.g., prs(shift), dly(3), fre(5)).
    • Commands are separated by semicolons.
    • The definition must end with 'save as' followed by the desired macro name.
    • The function accounts for extra whitespace, surrounding quotes, and case variations.
    
    Example:
      mcm("prs(shift); dly(3); prs(shift); dly(1); fre(5) save as fly and shoot")
    """
    try:
        content = content.strip().strip('"').strip("'")
        
        if "save as" not in content.lower():
            print("Macro creation command not properly formatted. Expected format: '<commands> save as <macro name>'")
            return (None, ())
        
        parts = re.split(r"\s*save as\s*", content, flags=re.IGNORECASE, maxsplit=1)
        if len(parts) != 2:
            print("Macro creation command not properly formatted. Expected format: '<commands> save as <macro name>'")
            return (None, ())
        commands_part, name_part = parts
        
        macro_name = name_part.strip().replace(" ", "-").lower()
        
        delimiter = ";" if ";" in commands_part else "then"
        command_list = [cmd.strip() for cmd in commands_part.split(delimiter) if cmd.strip()]
        
        # Save the macro data to a JSON file
        macro_data = {"name": macro_name, "commands": command_list}
        filename = os.path.join(MACRO_DIR, f"{macro_name}.json")
        with open(filename, "w") as f:
            json.dump(macro_data, f)
        print(f"Macro '{macro_name}' created with commands: {command_list}")
    except Exception as e:
        print(f"Error creating macro: {e}")
    return (None, ())

def run_macro(content):
    """
    Run a macro by name.
    The macro JSON file should contain a list of command strings,
    and each command is then processed using your existing command system.
    """
    macro_name = content.strip().replace(" ", "-").lower()
    filename = os.path.join(MACRO_DIR, f"{macro_name}.json")
    if not os.path.exists(filename):
        print(f"Macro '{macro_name}' not found.")
        return (None, ())
    try:
        with open(filename, "r") as f:
            macro_data = json.load(f)
        for cmd in macro_data["commands"]:
            print(f"Executing macro command: {cmd}")
            process_command(cmd)
    except Exception as e:
        print(f"Error running macro: {e}")
    return (None, ())

def get_macros():
    """Return a list of macro JSON files in MACROS_DIR (each representing a macro)."""
    try:
        return [f for f in os.listdir(MACROS_DIR) 
                if f.endswith('.json') and os.path.isfile(os.path.join(MACROS_DIR, f))]
    except Exception as e:
        print(_("Error reading MACROS_DIR:"), e)
        return []

available_macros = ", ".join(get_macros())

command_handlers = {
    "mcm": lambda content: (create_macro, (content,)),
    "mcr": lambda content: (run_macro, (content,))
}

commands_string = f"""
 mcm(content) - Create a macro. Format: "<command1>; <command2>; ...; <commandN> save as <macro name>" (Each command must be a valid token command separated by semicolons, and the definition must end with 'save as' followed by the macro name; e.g., mcm("prs(shift); dly(3); fre(5) save as flying shoot"))
 mcr(name)    - Run a macro with the given name (The name must match the macro defined during creation; Available macros: {available_macros})
"""