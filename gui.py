import conversion_utils
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import logging

logger = logging.getLogger(__name__)

def select_pac():
    tk.Tk().withdraw()
    pac_filename = tk.filedialog.askopenfilename(title="Select a .pac file",
                                                 filetypes=[("Pac files", "*.pac"), ("All Files", "*.*")])
    if pac_filename != "":
        try:
            conversion_utils.convert_files(pac_filename, "")
        except Exception as e:
            logger.critical(f"There was an issue converting {pac_filename}")
            logger.critical(e)


def select_mpc():
    tk.Tk().withdraw()
    mpc_filename = tk.filedialog.askopenfilename(title="Select a .mpc file",
                                                 filetypes=[("Mpc files", "*.mpc"), ("All Files", "*.*")])
    if mpc_filename != "":
        try:
            conversion_utils.convert_files("", mpc_filename)
        except Exception as e:
            logger.critical(f"There was an issue converting {mpc_filename}")
            logger.critical(e)

def select_folder():
    tk.Tk().withdraw()
    folder_path = tk.filedialog.askdirectory()
    if folder_path != "":
        try:
            conversion_utils.convert_folder(folder_path)
        except Exception as e:
            logger.warning(f"Exception caught: {e}")
            pass
        conversion_utils.display_results()

def init_interface():
    root = tk.Tk()
    root.title("UFC Undiputed 3 Model Converter")
    root.geometry("530x100")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("TButton",
                    font=("Arial", 12),
                    padding=10,
                    relief="flat",
                    foreground="black",
                    background="black")

    button_pac = ttk.Button(root, text="Select a .pac file", style="TButton", command=select_pac)
    button_pac.grid(row=1, column=0, padx=10, pady=15)

    button_mpc = ttk.Button(root, text="Select a .mpc file", style="TButton", command=select_mpc)
    button_mpc.grid(row=1, column=1, padx=10, pady=15)

    button_folder = ttk.Button(root, text="Select a folder", style="TButton", command=select_folder)
    button_folder.grid(row=1, column=2, padx=10, pady=15)

    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

    root.mainloop()