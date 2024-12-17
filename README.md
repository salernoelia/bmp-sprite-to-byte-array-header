# BMP to C/C++ Header Converter

A Python application that converts a series of BMP images into a C header file containing `uint16_t` arrays in RGB565 format, suitable for use in C/C++/Arduino projects. It was made for automating the bmp to byte array pipeline for displaying animated sprites

## Features

- **Automatic Folder Processing:** Reads all BMP files from a specified input folder.
- **Dynamic Header Generation:** Generates header file definitions based on the output filename.
- **RGB565 Conversion:** Converts 24-bit RGB images to 16-bit RGB565 format.
- **Organized Output:** Saves generated header files in an `output` directory, creating it if it doesn't exist.
- **Natural Sorting:** Ensures frames are ordered correctly (e.g., `frame10.bmp` comes after `frame9.bmp`).

## Setup Instructions

1. **Clone the Repository**

2. **Create and Activate a Virtual Environment (Optional but Recommended)**

   ```sh
   python -m venv .venv
   ```

Activate the virtual environment:

- **On Linux or MacOS:**

  ```sh
  source .venv/bin/activate
  ```

- **On Windows:**

  ```sh
  .venv\Scripts\activate
  ```

3. **Install Required Dependencies**

   ```sh
   pip install pillow
   ```

## Usage

1. **Organize Your BMP Files**

   - Place all your BMP images (e.g., `confused1.bmp`, `confused2.bmp`, ..., `confusedN.bmp`) into a single input folder, for example, `./input`.

2. **Run the Script**

   Make sure you set the correct resolution in hte script.

   ```sh
   python app.py <output_header.h> <input_folder>
   ```

   - **Arguments:**

     - `<output_header.h>`: Desired name for the output header file (e.g., `confused.h`).
     - `<input_folder>`: Path to the folder containing your BMP files (e.g., `./input`).

   - **Example:**

     ```sh
     python app.py lucky_smile.h ./input
     ```

3. **Output**

   - The script will generate the specified header file inside the `output` directory. If the `output` folder does not exist, it will be created automatically.

   - **Example Output Path:**

     ```
     ./output/lucky_smile.h
     ```

   - **Generated `lucky_smile.h` Structure:**

     ```c
     // lucky_smile.h
     #ifndef LUCKY_SMILE_H
     #define LUCKY_SMILE_H

     #include <Arduino.h>

     const uint16_t lucky_smile1[96 * 96] PROGMEM = {
         0x1234, 0x5678, /* ... more pixel data ... */
         // Each line contains 12 pixel values
     };

     const uint16_t lucky_smile2[96 * 96] PROGMEM = {
         /* ... pixel data ... */
     };

     // ... more image arrays ...

     const uint16_t* lucky_smile_sheet[] PROGMEM = { lucky_smile1, lucky_smile2, /* ... more arrays ... */ };
     const int lucky_smile_frameCount = sizeof(lucky_smile_sheet) / sizeof(lucky_smile_sheet[0]);

     #endif // LUCKY_SMILE_H
     ```

## Workflow

1. **Activate Virtual Environment**

   ```sh
   source .venv/bin/activate
   ```

2. **Install Dependencies**

   ```sh
   pip install pillow
   ```

3. **Run the Script**

   ```sh
   python app.py lucky_smile.h ./input
   ```

   - **Outcome:**
     - The header file `lucky_smile.h` will be created inside the `output` directory with all BMP frames converted to `uint16_t` arrays in RGB565 format.
     - The header will include an array of pointers to each frame and a frame count.

## Notes

- **Image Dimensions:** The script expects all BMP images to be `96x96` pixels. If images of different sizes are provided, a warning will be issued, but the script will attempt to process them regardless. For best results, ensure all images are consistently sized.

- **File Naming:** Ensure BMP filenames are structured to facilitate natural sorting (e.g., `frame1.bmp`, `frame2.bmp`, ..., `frame10.bmp`). This ensures frames are ordered correctly in the generated header.

- **Error Handling:**

  - The script will notify you if the input folder does not exist or contains no BMP files.
  - Ensure that the input paths and filenames are correct to avoid processing errors.

- **Customization:**
  - If you need to handle different image sizes or formats, consider modifying the script accordingly.
  - The `sanitize_variable_name` function ensures that variable names derived from filenames are valid C identifiers.

```

```
