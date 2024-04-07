import os
import tkinter as tk
from PIL import Image, ImageTk

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

        self.images = []
        self.current_image_index = 0
        self.load_images()
        
        # Binding keyboard events
        self.master.bind("<Left>", lambda event: self.prev_image())
        self.master.bind("<Right>", lambda event: self.next_image())

        # Update title to display image count
        self.title_init()

    def update_title(self):
        total_images = len(self.images)
        current_image = self.current_image_index
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
        image = Image.open(self.current_image_path)
        image.thumbnail((400, 400))  # Resize image to fit within a 400x400 box
        self.image_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_tk)

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

            

root = tk.Tk()
app = ImageFlickerGUI(root)
root.mainloop()