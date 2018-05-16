# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity

    s = ssim(imageA, imageB, multichannel=True)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("SSIM: %.2f" % (s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB)
    plt.axis("off")

    # show the images
    plt.show()

# load the images -- the original, the original + contrast,
# and the original + photoshop
eczema = cv2.imread("static/testing/eczema.PNG")
psoriasis = cv2.imread("static/testing/eczema2.jpeg")

# initialize the figure
fig = plt.figure("Images")
images = ("Eczema", eczema), ("Psoriasis", psoriasis)

# loop over the images
# for (i, (name, image)) in enumerate(images):
#     # show the image
#     ax = fig.add_subplot(1, 3, i + 1)
#     ax.set_title(name)
#     plt.imshow(image)
#     plt.axis("off")
#
# # show the figure
# plt.show()

# compare the images
compare_images(eczema, psoriasis, "Hives vs Psoriasis")
