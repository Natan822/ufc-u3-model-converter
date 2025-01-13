# UFC U3 Model Converter
This is a simple tool that can be used to convert UFC Undisputed 3 character models from PS3 to Xbox 360 or RPCS3 to Xenia.

## Requirements
- **Python** >= 3.12.8
- **ImageMagick** >= 7.1.1

## Dependencies
- **Wand** == 0.6.13 (used for resizing *.dds textures)

## Usage
1. Clone this repository:
```bash
git clone https://github.com/Natan822/ufc-u3-model-converter.git
``` 
2. Navigate to the project's directory where 'main.py' is located.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Execute 'main.py':
```bash
python main.py
``` 
5. **Optional**: Select a character's *.pac file.
6. **Optional**: Select a character's *.mpc file.
7. Done!  

If everything has run as expected, your selected files will be overwritten and converted to be ready to use on an Xbox 360 or Xenia's version of the game. A backup of the original files will also be created in the same folder under the name of {file_name}.bak.

## Credits
This project would not be possible without:
- The contributions of 'TheMMAVeteran' to the '[UFC Undisputed 3 Modding Guides](https://ufc-undisputed.fandom.com/wiki/UFC_Undisputed_3_Modding_Guides)' wiki.
- UUC's model ports of UDF's RPCS3 models which were used for reverse engineering.

## Known issues
- Converting certain models may not work due to problems decompressing their all.tex file.