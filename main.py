import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import random
import os
from RangeSlider import RangeSliderH
import sv_ttk

class SyntheticImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Synthetic Data Generator")
        
        sv_ttk.use_dark_theme()

        # Initialize variables
        self.background_images = [] # contains a list of image_path
        self.object_images = [] # contains a list of tuples (subfolder_name, image_path)

        self.scale_min_var = tk.DoubleVar(value=0.2)
        self.scale_max_var = tk.DoubleVar(value=1.0)

        self.obj_min_var = tk.DoubleVar(value=1.0)
        self.obj_max_var = tk.DoubleVar(value=10.0)

        self.rot_min_var = tk.DoubleVar(value=-90.0)
        self.rot_max_var = tk.DoubleVar(value=90.0)

        # The assigned value beside 1 is somehow not reflected on ttk.LabeledScale
        self.num_images_var = tk.IntVar(value=1)

        self.setup_ui()

    def setup_ui(self):

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        bg_button = ttk.Button(main_frame, text="Select Background Images", command=self.select_background_images)
        bg_button.grid(row=0, column=0, padx=10, pady=10)

        obj_button = ttk.Button(main_frame, text="Select Object Images Folder", command=self.select_object_image_folder)
        obj_button.grid(row=1, column=0, padx=10, pady=10)

        self.bg_label = ttk.Label(main_frame, text="0 Images Selected")
        self.bg_label.grid(row=0, column=1, padx=10, pady=10)

        self.obj_label = ttk.Label(main_frame, text="0 Classes Selected")
        self.obj_label.grid(row=1, column=1, padx=10, pady=10)
        
        self.create_slider_with_entry(main_frame, "Number of Images", self.num_images_var, 1, 100, row=2, column=0)
        self.create_range_slider_with_entries(main_frame, "Scale Range (Min-Max)", [self.scale_min_var, self.scale_max_var], 0.2, 3.0, 0.1, row=3)
        self.create_range_slider_with_entries(main_frame, "Objects per Image (Min-Max)", [self.obj_min_var, self.obj_max_var], 1, 20, 1, row=4)
        self.create_range_slider_with_entries(main_frame, "Rotation Range (Min-Max)", [self.rot_min_var, self.rot_max_var], -180, 180, 1, row=5)

        generate_button = ttk.Button(main_frame, text="Generate", command=self.generate_synthetic_images)
        generate_button.grid(row=6, column=0, columnspan=2, pady=20)

    def create_slider_with_entry(self, main_frame, label_text, variable, from_, to, row, column):
        ttk.Label(main_frame, text=label_text).grid(row=row, column=0, padx=10, pady=10)
        num_entry = ttk.Entry(main_frame, textvariable=variable, width=5, 
                              validate='all', validatecommand=(self.root.register(self.validate_digit), '%P'))
        num_entry.grid(row=row, column=1, padx=10, pady=10)  # Entry on the left
        try:
            slider = ttk.LabeledScale(main_frame, variable=variable, from_=from_, to=to)
        except:
            slider = ttk.Scale(main_frame, variable=variable, from_=from_, to=to)
        slider.grid(row=row, column=2, padx=10, pady=10)  # Slider to the right of the entry
        # Bind the entry to update the slider
        num_entry.bind("<Return>", lambda e: self.update_slider_from_entry(slider, variable, from_, to))

    def create_range_slider_with_entries(self, main_frame, label_text, variables, min_val, max_val, step_size, row):
        ttk.Label(main_frame, text=label_text).grid(row=row, column=0, padx=10, pady=10)
        min_entry = ttk.Entry(main_frame, textvariable=variables[0], width=5, 
                              validate='all', validatecommand=(self.root.register(self.validate_digit), '%P'))
        min_entry.grid(row=row, column=1, padx=5, pady=10)  # Entry for min value on the left
        range_slider = RangeSliderH(main_frame, variables=variables, min_val=min_val, max_val=max_val, 
                                    step_size=step_size, padX=18, Width=150, Height=50, bgColor='#1c1c1c', 
                                    font_family="Segoe UI Variable", font_size=11, font_color='#fafafa', 
                                    bar_color_inner="#57c8ff", bar_color_outer="#595959", bar_radius=10,
                                    line_s_color="#57c8ff", line_color="#9c9c9c", line_width=4)
        range_slider.grid(row=row, column=2, pady=10)  # Slider in the middle
        max_entry = ttk.Entry(main_frame, textvariable=variables[1], width=5, 
                              validate='all', validatecommand=(self.root.register(self.validate_digit), '%P'))
        max_entry.grid(row=row, column=3, pady=10)  # Entry for max value on the right
        
        # Bind entries to update the slider when the entry value changes with limits
        min_entry.bind("<Return>", lambda e: self.update_range_slider_from_entries(range_slider, variables[0], variables[1], min_val, max_val))
        max_entry.bind("<Return>", lambda e: self.update_range_slider_from_entries(range_slider, variables[0], variables[1], min_val, max_val))

    def validate_digit(self, P):
        if P is None: 
            return False
        try:
            float(P)
            return True
        except ValueError:
            return False
    
    # Function to limit the entry value based on min_val and max_val
    def limit_value(self, var, min_val, max_val):
        try:
            value = float(var.get())
            if value < min_val:
                var.set(min_val)
            elif value > max_val:
                var.set(max_val)
        except tk.TclError:
            var.set(min_val)

    # Function to update the slider when the entry value changes and apply value limits
    def update_slider_from_entry(self, slider, var, min_val, max_val):
        self.limit_value(var, min_val, max_val)  # Ensure the value is within the limit
        slider.set(float(var.get()))  # Update the slider

    def update_range_slider_from_entries(self, range_slider, min_var, max_var, min_val, max_val):
        self.limit_value(min_var, min_val, max_var.get())  # Limit min entry value based on slider's range
        self.limit_value(max_var, min_var.get(), max_val)  # Limit max entry value based on slider's range
        range_slider.forceValues([float(min_var.get()), float(max_var.get())])  # Update the range slider

    def select_background_images(self):
        """Open file dialog to select background images."""
        self.background_images = filedialog.askopenfilenames(title="Select Background Images")
        self.update_label(self.bg_label, self.background_images)
    
    def select_object_image_folder(self):
        """Open file dialog to select the main object image folder and process the subfolders"""
        self.main_folder = filedialog.askdirectory(title="Select Main Object Image Folder")
        
        if not self.main_folder:  # If no folder is selected, return early
            return
        
        subfolder_list = [subfolder for subfolder in os.listdir(self.main_folder) 
                          if (os.path.isdir(os.path.join(self.main_folder, subfolder)) and subfolder.isdigit())] # Filters for folder that is a digit
        
        for subfolder_name in subfolder_list:
            subfolder_path = os.path.join(self.main_folder, subfolder_name)
            for file_name in os.listdir(subfolder_path):
                if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    image_path = os.path.join(subfolder_path, file_name)
                    self.object_images.append((subfolder_name, image_path))

        #print(self.object_images)  # For debugging
        self.obj_label['text'] = f"{len(subfolder_list)} Classes Selected"

    def select_object_images(self): # Deprecated
        """Open file dialog to select object images."""
        self.object_images = filedialog.askopenfilenames(title="Select Object Images")
        self.update_label(self.obj_label, self.object_images)

    def update_label(self, label, image_list):
        """Update the label to show how many images were selected."""
        label['text'] = f"{len(image_list)} Images Selected"

    def generate_synthetic_images(self):
        """Generate synthetic images based on the selected parameters."""
        # Read slider values
        num_images = int(self.num_images_var.get())
        scale_min = self.scale_min_var.get()
        scale_max = self.scale_max_var.get()
        obj_min = int(self.obj_min_var.get())
        obj_max = int(self.obj_max_var.get())
        rot_min = self.rot_min_var.get()
        rot_max = self.rot_max_var.get()

        output_folder = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Generating Images")
        progress_window.geometry("400x100")

        progress_label = tk.Label(progress_window, text="Generating images, please wait...")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        progress_bar["maximum"] = num_images

        for i in range(num_images):
            bg_img_path = random.choice(self.background_images)
            obj_count = random.randint(obj_min, obj_max)
            self.create_synthetic_image(bg_img_path, obj_count, scale_min, scale_max, rot_min, rot_max, i, output_folder)

            # Update the progress bar
            progress_bar["value"] = i + 1
            progress_window.update()

        # Close the progress window automatically after 1 sec
        progress_window.after(1000, progress_window.destroy)

    def create_synthetic_image(self, bg_img_path, obj_count, scale_min, scale_max, rot_min, rot_max, img_num, output_folder):
        """Generate one synthetic image with randomized objects and save."""
        bg_img = Image.open(bg_img_path)
        bg_width, bg_height = bg_img.size

        labels = []

        # Loop to add objects
        for _ in range(obj_count):
            class_idx, obj_img_path = random.choice(self.object_images)
            obj_img = Image.open(obj_img_path)
     
            # Alpha Channel is required for pasting with .paste
            if obj_img.mode != 'RGBA':
                obj_img = obj_img.convert('RGBA')
                
            # Randomize rotation
            rot_ang = random.uniform(rot_min, rot_max)
            obj_img = obj_img.rotate(rot_ang, expand=True)

            # Randomize scale
            scale_factor = random.uniform(scale_min, scale_max)
            obj_width = int(obj_img.width * scale_factor)
            obj_height = int(obj_img.height * scale_factor)
            obj_img = obj_img.resize((obj_width, obj_height))

            # Skip if the object is larger than background
            if bg_width - obj_width < 0 or bg_height - obj_height < 0:
                messagebox.showerror("Error", f"Object size {obj_width}x{obj_height} is larger than BG size {bg_width}x{bg_height}, normalization is recommended")
                return
            
            # Randomize position
            pos_x = random.randint(0, bg_width - obj_width)
            pos_y = random.randint(0, bg_height - obj_height)

            bg_img.paste(obj_img, (pos_x, pos_y), obj_img)

            # Calculate normalized values for the YOLO label
            # YOLO format is: class x_center y_center width height
            x_center = (pos_x + obj_width / 2) / bg_width  
            y_center = (pos_y + obj_height / 2) / bg_height
            norm_width = obj_width / bg_width
            norm_height = obj_height / bg_height

            labels.append(f"{class_idx} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")

        output_path = os.path.join(output_folder, f"synthetic_{img_num}.png")
        bg_img.save(output_path)

        label_path = os.path.join(output_folder, f"synthetic_{img_num}.txt")
        with open(label_path, "w") as f:
            f.write("\n".join(labels) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntheticImageGenerator(root)
    root.mainloop()
