import os
import json
from datetime import datetime

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
            if self.gui.save_option_var.get() == 1:  # Save individual files
                self.save_individual_annotation(label, folder_path)
            else:  # Save one JSON file
                self.save_json_annotation(label, folder_path)

    def save_individual_annotation(self, label, folder_path):
        # Get bounding box coordinates
        xmin = min(self.gui.start_x, self.gui.end_x)
        ymin = min(self.gui.start_y, self.gui.end_y)
        xmax = max(self.gui.start_x, self.gui.end_x)
        ymax = max(self.gui.start_y, self.gui.end_y)

        # Create annotation dictionary
        annotation = {
            "label": label,
            "bounding_box": {
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax
            }
        }

        # JSON filename for the current image
        json_filename = os.path.splitext(self.gui.images[self.gui.current_image_index])[0] + ".json"

        # If the JSON file already exists, load existing annotations
        if os.path.exists(json_filename):
            with open(json_filename, "r") as f:
                annotations = json.load(f)
        else:
            annotations = []

        # Append the new annotation to the list
        annotations.append(annotation)

        # Save annotations back to the JSON file
        with open(json_filename, "w") as f:
            json.dump(annotations, f)

        timestamp = datetime.now().strftime("%d/%m  %H:%M:%S")
        # Get the base name of the saved file
        saved_file_basename = os.path.basename(json_filename)
        # Construct the message string
        message = f"{timestamp} {saved_file_basename}: {label} Saved ({folder_path})"
        self.gui.update_message(message)

    def save_json_annotation(self, label, folder_path):
        # Create annotation dictionary for the current image
        annotation = {
            "image_filename": os.path.basename(self.gui.images[self.gui.current_image_index]),
            "label": label,
            "bounding_box": {
                "xmin": self.gui.start_x,
                "ymin": self.gui.start_y,
                "xmax": self.gui.end_x,
                "ymax": self.gui.end_y
            }
        }

        json_filename = "annotations.json"
        if os.path.exists(json_filename):
            # Load existing annotations if the file already exists
            with open(json_filename, "r") as f:
                annotations = json.load(f)
        else:
            annotations = []

        # Append the new annotation to the list
        annotations.append(annotation)

        # Save annotations to JSON file
        with open(json_filename, "w") as f:
            json.dump(annotations, f)

        timestamp = datetime.now().strftime("%d/%m %H:%M:%S")
        # Get the base name of the saved file
        saved_file_basename = os.path.basename(json_filename)
        # Construct the message string
        message = f"{timestamp} {saved_file_basename}: {label} Saved ({folder_path})"
        self.gui.update_message(message)
