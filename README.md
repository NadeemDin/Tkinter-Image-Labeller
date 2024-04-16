## Tkinter Object Labeller / Object Mapper / Bounding Box to .Json.

WORK IN PROGRESS - This is currently a quick draft

## Purpose:
This is my attempt at creating a tool to help me label images with bounding boxes as part of a larger project to build my own object detection methods from scratch.

<b> Essentially you draw a bounding box, hit save and it generates a .json file with data surrounding the bb and the image.</b>

![GUI](https://raw.githubusercontent.com/NadeemDin/Tkinter-Image-Labeller/main/README-images/GUI.png)


## How it works:
0. Run `main.py`

1. Load images from desired folder
2. Draw bounding box using the mouse from top left to bottom right of desired object. (can only draw one box per save)
3. Enter a class label.
4. Select a save option:
    - Save to 'file_name'.json - this allows the user to create or append to a .json specifically for that one image, the file will be named after the image and contain all boundingbox data for that image. data is appended to the file per save.
    - Save to master_data.json - this allows the user to write/save data for every boundingbox/image in one place. data is appended to the file per save.
5. Hit the save button or press 'Enter'.
5. Repeat steps 2,3,5 if you have mutiple labels/bounding boxes you wish to add. 
6. Navigate to the next or previous images using the buttons or left/right keys. - The GUI window title will update to let you know which image youre viewing and how many remain (e.g. 1/16 - first image out of 16 total)

Upon saving the boundingbox data  a 'data' folder will be generated within the folder containing the images, within this folder all data will be saved in the .json format - this keeps everything in one place:

Example of saved output:

```
[
  {
    "file_path": "C:\\...",
    "width": 318,
    "height": 159,
    "annotations": [
      {
        "bbox": [
          68,
          17,
          231,
          142
        ],
        "label": "cat"
      }
    ]
  }
]
 ````

Using the plotter.py to parse the .json file of cat.json to see if this works, results in this:

![plot_BB](https://raw.githubusercontent.com/NadeemDin/Tkinter-Image-Labeller/main/README-images/plottingBB.png)


Currently the GUI fails to function correctly with FULL WINDOW SCREENSHOT sized images - im going to attempt to work around this, it might be a case of altering the GUI UI/UX or potentially scaling the images. 


## Usage:


### Dependencies
- Python 3.x

### External Libraries
- **PIL (Python Imaging Library)**: Used for image processing.
- **matplotlib**: Used for plotting and visualization.
- **tkinter**: Used for building the graphical user interface (GUI).

### Python Modules
- **os**: Used for interacting with the operating system, e.g., file operations.
- **json**: Used for JSON serialization and deserialization.
- **datetime**: Used for working with dates and times.
- **tkinter**: Used for creating the GUI.
- **gui_design.ImageFlickerGUI**: Custom module for GUI design (assuming `gui_design` is a package containing `ImageFlickerGUI`).
- **functionality.Functionality**: Custom module for functionality (assuming `functionality` is a package containing `Functionality`).

### External Libraries (Additional)
- **filedialog** (from tkinter): Used for file dialog functionalities.
- **ImageDraw** (from PIL): Used for drawing on images.

### Installation
You can install the required dependencies using pip install after cloning the repo.

the only files you really need are:

1. main.py - self explanatory
2. functionality.py - contains all the save functionality
3. gui_design.py - contains all the gui design aspects, buttons, message screen etc.

 

