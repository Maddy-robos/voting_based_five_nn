import os
from PIL import Image
import matplotlib.pyplot  as plt
import numpy as np

image_folders = [
    'images/DRFI/',
    'images/DSR/',
    'images/GMR/',
    'images/MC/',
    'images/RBD/',
    'images/GTRUTH/',
    'images/OP/'
]
output_folder = 'images/CMP/'

cnt = 0
for filename in os.listdir(image_folders[0]):
    cnt += 1

for file_count in range(cnt):
    folder = image_folders[0]
    image = Image.open(os.path.join(folder)+os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(331)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('DRFI Output')

    folder = image_folders[1]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(332)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('DSR Output')

    folder = image_folders[2]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(333)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('GMR Output')

    folder = image_folders[3]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(334)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('MC Output')

    folder = image_folders[4]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(335)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('RBD Output')

    folder = image_folders[5]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(336)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Ground Truth')

    folder = image_folders[6]
    image = Image.open(os.path.join(folder) + os.listdir(os.path.join(folder))[file_count])
    ax = plt.subplot(338)
    ax.imshow(np.asarray(image), cmap=plt.cm.gray)
    ax.axis('off')
    ax.set_title('Our Output')

    plt.savefig(os.path.join(output_folder) + str(file_count+1) + ".png")
    # plt.show()
