import os
import shutil
import argparse
import subprocess
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
args = parser.parse_args()

search_list = [
    'idea_community_logo.png',
    'idea_community_logo@2x.png',
    'idea_logo@2x.png',
    'idea_logo@2x.png'
]


class Patcher:
    def __init__(self, target):
        self.target = target

    def patch(self, rp_image):
        bd = os.getcwd()
        tmpdir = os.path.join(bd, "tmp_patch")
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir)

        file_name = os.path.basename(self.target)
        shutil.copyfile(self.target, os.path.join(tmpdir, file_name))
        os.chdir(tmpdir)
        result = subprocess.run(['jar', '-tf', file_name], capture_output=True, text=True)

        tg = []
        for x in result.stdout.split('\n'):
            if x in search_list:
                tg.append(x)

        if len(tg) != 0:
            subprocess.run(['jar', '-xvf', file_name] + tg)
            for x in tg:
                image = Image.open(x)
                sz = image.size
                image.close()
                t = rp_image.resize(sz)
                os.remove(x)
                t.save(x)
            subprocess.run(['jar', '-uvf', file_name] + tg)
            os.remove(self.target)
            shutil.copyfile(file_name, self.target)

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
p.patch(rs)
print("Done")
