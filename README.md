# UFC U3 Model Converter
This is a simple tool that can be used to convert UFC Undisputed 3 character models from PS3 to Xbox 360 or RPCS3 to Xenia.

## Requirements
- [**Python**](https://www.python.org/downloads/) (only required if using the command-line method) >= 3.12.8 
- [**ImageMagick**](https://imagemagick.org/script/download.php) >= 7.1.1

## Installation
> Note: Make sure you already have the requirements installed before following these steps.
### Option 1: Using the executable(Windows only)
1. Download and extract the latest release under the [Releases page](https://github.com/Natan822/ufc-u3-model-converter/releases).
2. Run the `ufc-converter-win64.exe` file.
### Option 2: Using the CLI

#### Dependencies
- **Wand** == 0.6.13 (used for resizing *.dds textures)  

#### Instructions
1. Either:
   - Clone this repository:
    ```bash
    git clone https://github.com/Natan822/ufc-u3-model-converter.git
    ``` 
   - Or download and extract the latest release's source code under the [Releases page](https://github.com/Natan822/ufc-u3-model-converter/releases).
2. Navigate to the project's directory where `main.py` is located.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Execute `main.py`:
```bash
python main.py
``` 
## Usage
1. Choose whether you want to convert a single `*.pac` or `*.mpc` file or a whole folder.
![main window's screenshot](/images/main-window.png)
> Note: Converting a folder is going to recursively look for *.pac and *.mpc files and folders within a selected folder.

2. Select the file/folder to be converted.
3. Done!  

If everything has run as expected, your selected files will be overwritten and converted to be ready to use on an Xbox 360 or Xenia's version of the game. A backup of the original files will also be created in the same folder under the name of {file_name}.bak.

## Credits
This project would not be possible without:
- The contributions of 'TheMMAVeteran' to the '[UFC Undisputed 3 Modding Guides](https://ufc-undisputed.fandom.com/wiki/UFC_Undisputed_3_Modding_Guides)' wiki.
- UUC's model ports of UDF's RPCS3 models which were used for reverse engineering.

## Known issues
- Fixed. ~~Converting certain models may not work due to problems decompressing their all.tex file.~~
- Conversion of Pride fighters is not yet supported.