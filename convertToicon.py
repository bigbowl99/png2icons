import os
from tkinter import Tk, filedialog, messagebox
from PIL import Image

def select_png_file():
    """
    Opens a file dialog for the user to select a PNG file.
    Returns the selected file path or None if cancelled.
    """
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a PNG file",
        filetypes=[("PNG files", "*.png")]
    )
    root.destroy()
    return file_path if file_path else None

def get_resampling_filter():
    """
    Determines the appropriate resampling filter based on Pillow version.
    Returns the resampling filter to use.
    """
    try:
        # For Pillow >= 10.0.0
        return Image.Resampling.LANCZOS
    except AttributeError:
        # For Pillow < 10.0.0
        return Image.LANCZOS

def convert_to_ico(png_path, sizes):
    """
    Converts a PNG file to ICO files of specified sizes.
    
    Parameters:
    - png_path (str): The path to the original PNG file.
    - sizes (list): A list of integer sizes for the ICO files.
    """
    try:
        # Open the original PNG image
        img = Image.open(png_path)
        
        # Ensure the image has an alpha channel
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get the appropriate resampling filter
        resample_filter = get_resampling_filter()
        
        # Get the directory and base name of the original file
        directory, filename = os.path.split(png_path)
        basename, _ = os.path.splitext(filename)
        
        for size in sizes:
            # Resize the image using the determined resampling filter
            resized_img = img.resize((size, size), resample_filter)
            
            # Debug: Print the size of the resized image
            print(f"Resized image for {size}x{size}: {resized_img.size}")
            
            # Define the ICO file name
            ico_filename = f"{basename}-{size}.ico"
            ico_path = os.path.join(directory, ico_filename)
            
            # Save the resized image as ICO with explicit size
            resized_img.save(ico_path, format='ICO', sizes=[(size, size)])
            print(f"Saved {ico_path}")
        
        messagebox.showinfo("Success", "ICO files have been created successfully.")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    """
    Main function to execute the PNG to ICO conversion.
    """
    png_file = select_png_file()
    if png_file:
        sizes = [256, 128, 64, 32]
        convert_to_ico(png_file, sizes)
    else:
        print("No file selected.")

if __name__ == "__main__":
    # Print Pillow version for debugging
    import PIL
    print(f"Pillow version: {PIL.__version__}")
    main()
