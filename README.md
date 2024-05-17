# Python based Jetbrains IDE logo replacer script

## How to use
```sh
python main.py \
  [-w image_url_to_replace | -i image_path_to_replace] \
  -t jar_file_to_patch
```
> Only difference between `-i` and `-w` is, `-i` loads image from local disk, `-w` downloads image from url.

## Where is target?
#### Windows with toolbox: 
> ~\\AppData\\Local\\JetBrains\\Toolbox\\apps\\your_ide\\channel_name_here\\version_here\\lib\\jar_file_here.jar

#### MacOS with toolbox:
> ~/Applications/your_idea_appfile.app/Contents/lib/jar_file_here.jar
 
## What Jar to patch?
=> Its highly dependent to your environment/IDEs. But usually `app.jar` or `product.jar`
> I have plan to detect this with script.

## TODOs
 - resize image but remain its original resolution(with adding margin)
 - IDE jar detection

## Credits
- Thanks to [@Aikoyori and others for great logos](https://github.com/Aikoyori/ProgrammingVTuberLogos)
