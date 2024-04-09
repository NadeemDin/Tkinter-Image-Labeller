import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def plot_image_with_bboxes(data):
    for entry in data:
        file_path = entry['file_path']
        image = Image.open(file_path)
        width, height = image.size

        fig, ax = plt.subplots(1)
        ax.imshow(image)

        for annotation in entry['annotations']:
            bbox = annotation['bbox']
            label = annotation['label']
            x, y, w, h = bbox
            rect = patches.Rectangle((x, y), w - x, h - y, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.text(x, y, label, color='r', fontsize=10, verticalalignment='bottom')

        plt.title(f'Image:, Width: {width}, Height: {height}')
        plt.axis('off')
        plt.show()

# JSON data provided
# JSON data provided
json_data = [
  {
    "file_path": "C:\\Users\\Pyrex_000\\Desktop\\github_projects\\Tkinter-Image-Labeller\\images\\cat.png",
    "width": 318,
    "height": 159,
    "annotations": [
      {
        "bbox": [
          56,
          6,
          235,
          140
        ],
        "label": "cat"
      }
    ]
  }
]
