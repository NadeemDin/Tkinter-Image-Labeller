import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from functionality import Functionality

class ImageFlickerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Flicker")

        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        # Button frame to contain all buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=5)

        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(button_frame, text="Load Images", command=self.load_images)
        self.load_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(button_frame, text="Save bbox & Label data", command=self.save_annotation)
        self.save_button.pack(side=tk.LEFT)

        self.save_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.save_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

        self.save_label = tk.Label(self.save_frame, text="JSON File Save Options:", padx=5, pady=5)
        self.save_label.pack(side=tk.TOP)

        self.save_option_var = tk.IntVar(value=1)  # Default to save individual files
        self.save_option_individual = tk.Radiobutton(self.save_frame, text="Save to 'file_name'.json", variable=self.save_option_var, value=1)
        self.save_option_individual.pack(side=tk.LEFT, padx=10)

        self.save_option_json = tk.Radiobutton(self.save_frame, text="Save to master_data.json", variable=self.save_option_var, value=2)
        self.save_option_json.pack(side=tk.LEFT, padx=10)

        message_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        message_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.message_listbox = tk.Listbox(message_frame, height=3)
        self.message_listbox.pack(side=tk.LEFT,pady =(5,5), fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.message_listbox.yview)
        
        self.label_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.label_frame.pack(side=tk.BOTTOM, pady=5, fill=tk.X)

        self.label_text = tk.Label(self.label_frame, text="Enter object label:")
        self.label_text.pack(side=tk.TOP)

        self.label_entry = tk.Entry(self.label_frame, width=30)
        self.label_entry.pack(side=tk.BOTTOM, pady=(0,5))

        self.images = []
        self.current_image_index = 0

        # Binding keyboard events
        self.master.bind("<Left>", lambda event: self.prev_image())
        self.master.bind("<Right>", lambda event: self.next_image())
        self.master.bind("<Return>", self.save_annotation)
        
        self.image_label.bind("<Button-1>", self.start_drag)
        self.image_label.bind("<B1-Motion>", self.drag)
        self.image_label.bind("<ButtonRelease-1>", self.end_drag)

        # Initialize variables for tracking mouse drag
        self.dragging = False
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Update title to display image count
        self.update_title()

        # Functionality
        self.func = Functionality(self)

    def update_title(self):
        total_images = len(self.images)
        current_image = self.current_image_index + 1
        if total_images > 0:
            image_filename = os.path.basename(self.images[self.current_image_index])
            self.master.title(f"ObjectMapper {current_image}/{total_images} - {image_filename}")
        else:
            self.master.title("ObjectMapper")

    def load_images(self):
        folder_path = filedialog.askdirectory(parent=self.master)
        if folder_path:
            self.images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg', '.png', '.jpeg'))]
            if self.images:
                self.current_image_index = 0
                self.show_image()
                self.update_title()
                self.master.update_idletasks()
                self.label_entry.focus_set()

    def show_image(self):
        self.image = Image.open(self.images[self.current_image_index])
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.tk_image, anchor="n")

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()
            self.update_title()

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()
            self.update_title()

    def start_drag(self, event):
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y
        self.end_x = event.x
        self.end_y = event.y

    def drag(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.draw_bounding_box()

    def end_drag(self, event):
        self.draw_bounding_box()
        self.dragging = False

    def draw_bounding_box(self):
        if self.dragging:
            image_copy = self.image.copy()
            draw = ImageDraw.Draw(image_copy)
            draw.rectangle([self.start_x, self.start_y, self.end_x, self.end_y], outline="red")
            tk_image_copy = ImageTk.PhotoImage(image_copy)
            self.image_label.config(image=tk_image_copy)
            self.image_label.image = tk_image_copy

    def save_annotation(self, event=None):
        self.func.save_annotation()

    def update_message(self, text):
        self.message_listbox.insert(0, text)
        self.scrollbar.config(command=self.message_listbox.yview)
