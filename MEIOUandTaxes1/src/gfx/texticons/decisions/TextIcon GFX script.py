import os

def generate_sprite_types(folder_name):
    # Template for the spriteTypes structure
    template = '''spriteType = {{
    name = "GFX_{name}"
    texturefile = "gfx//texticons//decisions//{folder_name}//{name}{ext}"
}}\n'''
    # Directory where the script is located
    directory = os.path.dirname(os.path.realpath(__file__))

    # File to write the output
    output_file = os.path.join(directory, "output.txt")

    with open(output_file, "w") as file:
        # Iterate over files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".dds") or filename.endswith(".png"):
                name, ext = os.path.splitext(filename)  # Separate file name and extension
                sprite_type = template.format(name=name, ext=ext, folder_name=folder_name)
                file.write(sprite_type)

def get_folder_name():
    while True:
        folder_name = input("Enter the folder name located in gfx\\texticons\\decisions you want referenced: ")
        if folder_name.strip():  # Check if folder_name is not empty
            return folder_name
        else:
            print("You must enter a valid folder name.")

# Get folder name with safety feature
folder_name = get_folder_name()

# Generate sprite types and write to file
generate_sprite_types(folder_name)
