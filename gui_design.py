import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
from functionality import Functionality

class ImageFlickerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Flicker")

        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.prev_button = tk.Button(self.master, text="Previous", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.master, text="Next", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT)

        self.save_frame = tk.Frame(self.master, bd=2, relief=tk.GROOVE)
        self.save_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.save_label = tk.Label(self.save_frame, text="Save Options:", padx=5, pady=5)
        self.save_label.pack(side=tk.TOP)

        self.save_option_var = tk.IntVar(value=1)  # Default to save individual files
        self.save_option_individual = tk.Radiobutton(self.save_frame, text="Individual Files", variable=self.save_option_var, value=1)
        self.save_option_individual.pack(side=tk.LEFT, padx=10)

        self.save_option_json = tk.Radiobutton(self.save_frame, text="One JSON File", variable=self.save_option_var, value=2)
        self.save_option_json.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_annotation)
        self.save_button.pack(side=tk.BOTTOM)
        

        #self.message_label = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        #self.message_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_listbox = tk.Listbox(self.master, yscrollcommand=self.scrollbar.set, height=3)
        self.message_listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.label_entry = tk.Entry(self.master, width=30)
        self.label_entry.pack(side=tk.BOTTOM, pady=5)

        self.images = []
        self.current_image_index = 0
        self.load_images()

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
        self.title_init()

        # Functionality
        self.func = Functionality(self)

    def update_title(self):
        total_images = len(self.images)
        current_image = self.current_image_index + 1
        self.master.title(f"Image Flicker {current_image}/{total_images}")

    def title_init(self):
        total_images = len(self.images)
        current_image = self.current_image_index + 1
        self.master.title(f"Image Flicker {current_image}/{total_images}")

    def load_images(self):
        folder_path = "images"
        if os.path.exists(folder_path):
            self.images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg', '.png', '.jpeg'))]
            if self.images:
                self.show_image()

    def show_image(self):
        self.current_image_path = self.images[self.current_image_index]
        self.image = Image.open(self.current_image_path)
        #self.image.thumbnail((400, 400))  # Resize image to fit within a 400x400 box
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.tk_image)

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()
            self.title_init()

    def next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()
            self.title_init()

    def start_drag(self, event):
        # Record the starting coordinates of the mouse drag
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y
        self.end_x = event.x
        self.end_y = event.y

    def drag(self, event):
        # Update the end coordinates of the mouse drag
        self.end_x = event.x
        self.end_y = event.y
        self.draw_bounding_box()

    def end_drag(self, event):
        # Draw bounding box when mouse drag ends
        self.draw_bounding_box()
        self.dragging = False

    def draw_bounding_box(self):
        if self.dragging:
            # Draw bounding box on the image
            image_copy = self.image.copy()
            draw = ImageDraw.Draw(image_copy)
            draw.rectangle([self.start_x, self.start_y, self.end_x, self.end_y], outline="red")
            tk_image_copy = ImageTk.PhotoImage(image_copy)
            self.image_label.config(image=tk_image_copy)
            self.image_label.image = tk_image_copy  # Keep a reference to avoid garbage collection

    def save_annotation(self, event=None):
        self.func.save_annotation()

    def update_message(self, text):
        self.message_listbox.insert(0, text)
        self.scrollbar.config(command=self.message_listbox.yview)
