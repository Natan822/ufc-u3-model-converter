import tkinter.filedialog
import conversion_utils
import tkinter as tk
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    tk.Tk().withdraw()
    pac_filename = tk.filedialog.askopenfilename(title="Select a .pac file",
                                   filetypes=[("Pac files", "*.pac"), ("All Files", "*.*")])
    mpc_filename = tk.filedialog.askopenfilename(title="Select a .mpc file",
                                   filetypes=[("Mpc files", "*.mpc"), ("All Files", "*.*")])
    conversion_utils.convert_files(pac_filename, mpc_filename)

if __name__ == '__main__':
    main()