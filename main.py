import tkinter as tk
from gui_design import ImageFlickerGUI

def main():
    root = tk.Tk()
    app = ImageFlickerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
