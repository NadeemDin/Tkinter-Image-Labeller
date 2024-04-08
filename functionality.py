import os
import json
from datetime import datetime
from PIL import Image

class Functionality:
    def __init__(self, gui):
        self.gui = gui

    def save_annotation(self):
        if self.gui.start_x is not None and self.gui.start_y is not None and self.gui.end_x is not None and self.gui.end_y is not None:
            label = self.gui.label_entry.get().strip()
            if not label:
                self.gui.update_message("Please enter a label for the bounding box.")
                return
            folder_path = os.path.dirname(self.gui.images[self.gui.current_image_index])
            data_folder_path = os.path.join(folder_path, "data")
            if not os.path.exists(data_folder_path):
                os.makedirs(data_folder_path)
            if self.gui.save_option_var.get() == 1:  # Save individual files
                self.save_individual_json(label, data_folder_path)
            else:  # Save one JSON file
                self.save_master_json(label, data_folder_path)

    def save_individual_json(self, label, folder_path):
        # Get bounding box coordinates
        xmin = min(self.gui.start_x, self.gui.end_x)
        ymin = min(self.gui.start_y, self.gui.end_y)
        xmax = max(self.gui.start_x, self.gui.end_x)
        ymax = max(self.gui.start_y, self.gui.end_y)

        # Create annotation dictionary
        annotation = {
            "bbox": [xmin, ymin, xmax, ymax],
            "label": label
        }

        # Initialize annotations if not already present
        if not hasattr(self.gui, 'annotations'):
            self.gui.annotations = []

        # Add annotation to the list
        self.gui.annotations.append(annotation)

        # Get the file path of the current image
        file_path = self.gui.images[self.gui.current_image_index]

        # Get image width and height
        with Image.open(file_path) as img:
            width, height = img.size

        # Add image data if not already present
        image_data = [{
            "file_path": os.path.join(folder_path, os.path.basename(file_path)),
            "width": width,
            "height": height,
            "annotations": self.gui.annotations
        }]
        
        # Append image data to JSON file
        json_filename = os.path.join(folder_path, os.path.splitext(os.path.basename(file_path))[0] + ".json")
        with open(json_filename, "w") as f:
            json.dump(image_data, f, indent=2)
            
        # Get the base name of the saved file
        saved_file_basename = os.path.basename(json_filename)

        timestamp = datetime.now().strftime("%d/%m  %H:%M:%S")
        message = (f"{timestamp}, File: {os.path.basename(file_path)}, label: {label}, Saved to: {saved_file_basename}, Location: ({folder_path})")
        self.gui.update_message(message)

    def save_master_json(self, label, folder_path):
        # Get the file path of the current image
        file_path = self.gui.images[self.gui.current_image_index]

        # Get image width and height
        with Image.open(file_path) as img:
            width, height = img.size

        # Create annotation dictionary for the current image
        annotation = {
            "bbox": [self.gui.start_x, self.gui.start_y, self.gui.end_x, self.gui.end_y],
            "label": label
        }

        # Check if an entry for the current image already exists in the JSON data
        json_filename = os.path.join(folder_path, "master_data.json")
                
        if os.path.exists(json_filename):
            with open(json_filename, "r") as f:
                all_data = json.load(f)
            
            # Check if there's an entry for the current image
            found = False
            for image_data in all_data:
                if image_data["file_path"] == os.path.join(folder_path, os.path.basename(file_path)):
                    # Append the annotation to the existing entry
                    image_data["annotations"].append(annotation)
                    found = True
                    break
            
            # If no entry was found, create a new one
            if not found:
                image_data = {
                    "file_path": os.path.join(folder_path, os.path.basename(file_path)),
                    "width": width,
                    "height": height,
                    "annotations": [annotation]
                }
                all_data.append(image_data)
        else:
            # If the JSON file doesn't exist, create a new one with the annotation data
            all_data = [{
                "file_path": os.path.join(folder_path, os.path.basename(file_path)),
                "width": width,
                "height": height,
                "annotations": [annotation]
            }]

        # Get the base name of the saved file
        saved_file_basename = os.path.basename(json_filename)

        # Save the updated JSON data to the file
        with open(json_filename, "w") as f:
            json.dump(all_data, f, indent=2)

        timestamp = datetime.now().strftime("%d/%m %H:%M:%S")
        message = (f"{timestamp}, File: {os.path.basename(file_path)}, label: {label}, Saved to: {saved_file_basename}, Location: ({folder_path})")
        self.gui.update_message(message)
