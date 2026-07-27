import json


with open("/Users/adingates/dev/juno-pipeline/config/examples/project.json") as f:
    config = json.load(f)

with open("/Users/adingates/dev/juno-pipeline/config/examples/shot.json") as f:
    shot = json.load(f)
    shot.pop("$schema", None)

# Takes a given string and returns it with green coloring
def green_text(text):
    return f"\033[92m{text}\033[0m"

# Takes a given string and returns it with red coloring
def red_text(text):
    return f"\033[91m{text}\033[0m"



# print_dict is a function that prints out all of the keys and values of a given dictionary, including nested dictionaries.
def print_dict(config, prefix=""):

    if isinstance(config, dict):

        for key, value in config.items():
            new_prefix = f"{prefix} -> {key}" if prefix else key

            if isinstance(value, dict):

                print_dict(value, new_prefix)

            else:
                print(new_prefix, "==", green_text(value))

    else:
        print(red_text("'print_dict' Requires a dictionary. No dictionary given."))
            
        



# deep_merge takes two dictionaries, a base and an override, and replaces the values of the base dictionary with the override. This worked on nested dictionaries.
def deep_merge(base, override):

    result = base.copy()

    for key, value in override.items():

        if isinstance(value, dict):

            #print(f"value is {value}")                                                                            #Debugging print statement
            #print(f"base is {result[key]}")                                                                       #Debugging print statement
            
            result[key] = deep_merge(result[key], value)

        else:

            
             
            #print(f"Overriding base value of '{key}' from {red_text(result[key])} to {green_text(value)}")        #Debugging print statement

            result[key] = value


    return result



#print_dict(config)
new_config = deep_merge(config, shot)
#print(config)
print_dict(new_config)





    