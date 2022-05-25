from argparse import ArgumentParser

import numpy as np
import PIL
from PIL.Image import Image
from scipy import fft

Q = np.array([[16, 11, 10, 16,  24,  40,  51,  61],
              [12, 12, 14, 19,  26,  58,  60,  55],
              [14, 13, 16, 24,  40,  57,  69,  56],
              [14, 17, 22, 29,  51,  87,  80,  62],
              [18, 22, 37, 56,  68, 109, 103,  77],
              [24, 25, 55, 64,  81, 104, 113,  92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 102,  99]])


def run() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("FILE")

    args = arg_parser.parse_args()

    decoded(*encoded(PIL.Image.open(args.FILE))).show()


def encoded(image: Image) -> tuple[Image]:
    # Make height/width multiples of eight to simplify later
    image = trimmed(image)

    Y, Cb, Cr = image.convert("YCbCr").split()

    B = np.array(Y, dtype="int")

    for block in blockized(B):
        block[:] = quantized(spectrum(block))

    return (B, downsampled(Cb), downsampled(Cr))
            
        
def decoded(B, Cb: Image, Cr: Image) -> Image:
    for block in blockized(B):
        block[:] = pixels(unquantized(block))

    Y = PIL.Image.fromarray(B.astype("byte"), mode="L")

    return PIL.Image.merge("YCbCr", (Y, upsampled(Cb), upsampled(Cr)))


def trimmed(image: Image) -> Image:
    return image.crop((0, 0, (image.width//8)*8, (image.height//8)*8))


def blockized(arr, size=8):
    height, width = arr.shape

    for i in range(height//size):
        for j in range(width//size):
            yield block(arr, i, j, size=size)


def block(arr, i, j, size=8):
    return arr[size*i:size*(i + 1), size*j:size*(j + 1)]


def spectrum(pxs):
    return fft.dctn(pxs - 128)


def quantized(spectrum):
    return np.divide(spectrum, Q).round()


def unquantized(spectrum):
    return np.multiply(spectrum, Q)


def downsampled(image: Image, n=2) -> Image:
    return image.resize((image.width//n, image.height//n), PIL.Image.NEAREST)


def upsampled(image: Image, n=2) -> Image:
    return image.resize((image.width*n, image.height*n), PIL.Image.NEAREST)


def pixels(spectrum):
    return fft.idctn(spectrum) + 128
