import os
import shutil
import argparse
import subprocess
import platform
from PIL import Image

'''
 Where is target?
 Windows with toolbox: ~\\AppData\\Local\\JetBrains\\Toolbox\\apps\\your_ide\\channel_name_here\\version_here\\lib\\jar_file_here.jar
 MacOS with toolbox: ~/Applications/your_idea_appfile.app/Contents/lib/jar_file_here.jar
 
 What Jar to patch?
 Its highly dependent to your environment/IDEs. 
 I have plan to detect this with script.
'''

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', dest='target', help='Location of idea')
parser.add_argument('-i', '--image', dest='image', help='Image file to replace')
parser.add_argument('-w', '--web-image', dest='web_image', help='Image from web')
parser.add_argument('-m', '--method', dest='method', default='keep_resolution', help='keep_resolution or resize')
args = parser.parse_args()

search_list = [
    # IntellIJ Community(2024), inside app.jar
    ('app.jar', ['idea_community_logo.png', 'idea_community_logo@2x.png']),

    # IntellIJ Ultimate(2024), inside product.jar
    ('product.jar', ['idea_logo.png', 'idea_logo@2x.png']),

    # Rider(2024), inside product.jar
    ('product.jar', ['rider/artwork/release/splash.png', 'rider/artwork/release/splash@2x.png']),

    # CLion(2024), inside product.jar
    ('product.jar', ['artwork/clion_splash.png', 'artwork/clion_splash@2x.png']),
    
    # PyCharm Community(2024), inside app-client.jar
    ('app-client.jar', ['pycharm_core_logo.png', 'pycharm_core_logo@2x.png']),

    # RustRover(2024), inside product.jar
    ('product.jar', ['artwork/splash.png', 'artwork/splash@2x.png']),

    # WebStorm(2023, 2024), inside app.jar
    ('app.jar', ['artwork/webide_logo.png', 'artwork/webide_logo@2x.png']),
]


class Patcher:
    def __init__(self, target):
        if platform.system() == "Darwin":
            target = os.path.join(target, 'Contents')
        target = os.path.join(target, 'lib')

        self.target = []
        for x in search_list:
            jf = os.path.join(target, x[0])
            result = subprocess.run(['jar', '-tf', jf], capture_output=True, text=True)

            for sp in result.stdout.split('\n'):
                if sp in x[1]:
                    self.target.append((jf, sp))
                    print(f'Found {sp} at {x[0]}')

    @staticmethod
    def add_margin(pil_img, top, right, bottom, left, color):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top))
        return result

    def patch(self, rp_image, transform_mode="resize"):
        bd = os.getcwd()
        tmpdir = os.path.join(bd, "tmp_patch")
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)

        os.chdir(tmpdir)

        for j, img_path in self.target:
            file_name = os.path.join(tmpdir, os.path.basename(j))
            shutil.copyfile(j, file_name)

            subprocess.run(['jar', '-xvf', file_name, img_path])
            image = Image.open(img_path)
            sz = image.size
            image.close()

            if transform_mode == "resize":
                t = rp_image.resize(sz)
                os.remove(img_path)
                t.save(img_path)
            elif transform_mode == "keep_resolution":
                xs, ys = rp_image.size
                exs, eys = min(sz[0], sz[1] * xs // ys), min(sz[0] * ys // xs, sz[1])
                t = Patcher.add_margin(rp_image.resize((exs, eys)), (sz[1] - eys) // 2, (sz[0] - exs) // 2, (sz[1] - eys) // 2, (sz[0] - exs) // 2, 0)
                os.remove(img_path)
                t.save(img_path)

            subprocess.run(['jar', '-uvf', file_name, img_path])
            os.remove(j)
            shutil.copyfile(file_name, j)

        os.chdir(bd)
        shutil.rmtree(tmpdir)


p = Patcher(args.target)
if args.web_image is not None:
    import requests
    import io

    print("Downloading image...")
    rsp = requests.get(args.web_image)
    rs = Image.open(io.BytesIO(rsp.content))
else:
    print("Loading image from disk...")
    rs = Image.open(args.image)

print("Begin patch")
p.patch(rs, args.method)
print("Done")
