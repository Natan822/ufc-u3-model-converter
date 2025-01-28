from tkinter import messagebox
import sys

def imagemagick_not_installed():
    messagebox.showerror(title="UFC Undisputed 3 Model Converter",
                                 message="ImageMagick does not seem to be installed. Please make sure it is installed and try again.")
    sys.exit()