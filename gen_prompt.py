import json
import os


JSON_FILE_PATH = "./prompts/prompts.json"

def generate_prompts(plot_type, task_type, folder_path):
    # Load task descriptions from JSON file
    with open(JSON_FILE_PATH, 'r') as file:
        task_descriptions = json.load(file)
    
    # Get the specific task description
    task_description = task_descriptions.get(plot_type, {}).get(task_type, "")
    if not task_description:
        return []  # Return an empty list if the plot type or task type is not found
    
    # List all SVG files in the folder
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    
    # Initialize an empty list to hold the prompts
    prompts = []
    
    # Generate a prompt for each SVG file
    for svg_file in svg_files:
        # Read the SVG file contents
        with open(os.path.join(folder_path, svg_file), 'r') as file:
            svg_content = file.read()
        
        # Concatenate the task description and SVG content, separated by a newline
        prompt = f"{task_description}\n{svg_content}"
        
        # Add the prompt to the list
        prompts.append(prompt)
    
    return prompts

