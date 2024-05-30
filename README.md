# Python based Jetbrains IDE logo replacer script

## Use this at your risk!!!

## How to use
Required dependency: python, pillow

If you want to make patcher download image from web, you need requests module.
```sh
python main.py \
  [-w image_url_to_replace | -i image_path_to_replace] \
  -t appfile(mac) or directory(windows) to patch
```
> Only difference between `-i` and `-w` is, `-i` loads image from local disk, `-w` downloads image from url.

## Where is target?
#### Windows with toolbox: 
> ~\\AppData\\Local\\JetBrains\\Toolbox\\apps\\your_ide\\channel_name_here\\version_here

#### MacOS with toolbox:
> ~/Applications/your_appfile.app

## Credits
- Thanks to [@Aikoyori and others for great logos](https://github.com/Aikoyori/ProgrammingVTuberLogos)
