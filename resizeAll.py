import os
from PIL import Image

imageFolders = [
    'images/DRFI/',
    'images/DSR/',
    'images/GMR/',
    'images/MC/',
    'images/RBD/',
    'images/GTRUTH/'
]

for folder in imageFolders:
    for filename in os.listdir(folder):
        image = Image.open(os.path.join(folder, filename))
        image = image.resize((400, 300), Image.ANTIALIAS)
        image.save(os.path.join(folder) + filename)
