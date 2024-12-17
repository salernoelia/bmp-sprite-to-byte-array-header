import sys
from PIL import Image
import os
import glob
import re

# Set the resolution of the images
resolution = [96, 96] 

def rgb_to_565(r, g, b):
    """
    Convert 8-bit per channel RGB to 16-bit RGB565.
    """
    r5 = (r * 31) // 255
    g6 = (g * 63) // 255
    b5 = (b * 31) // 255
    return (r5 << 11) | (g6 << 5) | b5

def process_image(img_path):
    """
    Open an image, convert it to RGB, and transform it into a list of RGB565 values.
    """
    img = Image.open(img_path)
    img = img.convert("RGB")
    
    width, height = img.size
    if width != resolution[0] or height != resolution[1]:
        print(f"Warning: Image {img_path} is {width}x{height}, expected: {resolution[0]}x{resolution[1]}", file=sys.stderr)
    
    pixels = list(img.getdata())
    rgb565_values = [rgb_to_565(r, g, b) for (r, g, b) in pixels]
    return rgb565_values

def sanitize_variable_name(name):
    """
    Sanitize the image filename to create a valid C variable name.
    Replace invalid characters with underscores.
    """
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    sanitized = ''.join(c if c in valid_chars else '_' for c in name)
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    return sanitized

def generate_header(output_file, base_name, images):
    """
    Generate the header file with RGB565 arrays and frame information.
    """
    include_guard = f"{base_name.upper()}_H"

    with open(output_file, "w") as f:
        f.write(f"// {os.path.basename(output_file)}\n")
        f.write(f"#ifndef {include_guard}\n")
        f.write(f"#define {include_guard}\n\n")
        f.write("#include <Arduino.h>\n\n")

        for index, (name, data) in enumerate(images, start=1):
            array_name = f"{base_name}{index}"
            f.write(f"const uint16_t {array_name}[{resolution[1]} * {resolution[0]}] PROGMEM = {{\n")
            for i, val in enumerate(data):
                f.write(f"0x{val:04X}")
                if i < len(data) - 1:
                    f.write(", ")
                if (i + 1) % 12 == 0:
                    f.write("\n")
            if len(data) % 12 != 0:
                f.write("\n")
            f.write("};\n\n")
        
        array_names = ", ".join(f"{base_name}{i}" for i in range(1, len(images) + 1))
        sheet_array_name = f"{base_name}_sheet"
        frame_count_name = f"{base_name}_frameCount"
        f.write(f"const uint16_t* {sheet_array_name}[] PROGMEM = {{ {array_names} }};\n")
        f.write(f"const int {frame_count_name} = sizeof({sheet_array_name}) / sizeof({sheet_array_name}[0]);\n\n")
        f.write(f"#endif // {include_guard}\n")

def natural_sort_key(s):
    """
    Generate a key for natural sorting of filenames.
    Splits the string into parts of digits and non-digits.
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('(\d+)', os.path.basename(s))]

def main():
    if len(sys.argv) != 3:
        print("Usage: python app.py <output_header.h> <input_folder>")
        sys.exit(1)
    
    output_header = sys.argv[1]
    input_folder = sys.argv[2]

    if not os.path.isdir(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_header_path = os.path.join(output_dir, os.path.basename(output_header))
    
    bmp_pattern = os.path.join(input_folder, "*.bmp")
    bmp_files = glob.glob(bmp_pattern)
    
    if not bmp_files:
        print(f"No BMP files found in the folder '{input_folder}'.", file=sys.stderr)
        sys.exit(1)
    
    bmp_files.sort(key=natural_sort_key)
    
    base_name = os.path.splitext(os.path.basename(output_header))[0]
    sanitized_base = sanitize_variable_name(base_name)
    
    images_data = []
    for img_path in bmp_files:
        rgb565_array = process_image(img_path)
        images_data.append((sanitized_base, rgb565_array))
    
    generate_header(output_header_path, sanitized_base, images_data)
    print(f"Header file '{output_header_path}' generated successfully with {len(images_data)} frames.")

if __name__ == "__main__":
    main()
