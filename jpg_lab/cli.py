from argparse import ArgumentParser

from PIL import Image, ImageFilter


def run():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("FILE")

    args = arg_parser.parse_args()

    compress(Image.open(args.FILE))


def compress(img: Image) -> None:
    Y, Cb, Cr = img.convert("YCbCr").split()

    # This is re-upsampled so it can be recombined with Y channel
    Cb = (Cb.resize((img.width//2, img.height//2), Image.NEAREST)
            .resize((img.width, img.height), Image.NEAREST))
    Cr = (Cr.resize((img.width//2, img.height//2), Image.NEAREST)
            .resize((img.width, img.height), Image.NEAREST))

    Image.merge("YCbCr", [Y, Cb, Cr]).show()
