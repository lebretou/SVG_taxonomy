import os


# Function to process and save each SVG code string as an SVG file
def save_svg_files(svg_code_list, directory, filename_prefix):
    for i, code in enumerate(svg_code_list):
        # Remove the markdown code block syntax (if present) and replace \n with actual newlines
        clean_code = code.replace('```svg\n', '').replace('\n```', '').replace('\\n', '\n')
        
        # Define a filename for the SVG. Here, we simply use an index. You might want to use a more descriptive naming.
        filename = f"{filename_prefix}_{i}.svg"
        filepath = os.path.join(directory, filename)
        
        # Write the cleaned SVG code to a file
        with open(filepath, 'w') as file:
            file.write(clean_code)
        print(f"Saved: {filepath}")
