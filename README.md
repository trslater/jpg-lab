# JPG Lab

A lab for messing around with JPG compression techniques.

## Requirements

This project uses Poetry to manage dependencies.

## Installation

```
poetry install
```

## Usage

To start the web application:

```
poetry run python -m jpglab serve
```

For more detailed usage instructions:

```
poetry run python -m jpglab -h
```

## Todo

### App

-   [x] Upload images

### Lib

-   [x] Image reading
-   [x] YCbCr conversion
-   [x] Downsampling
-   [x] DCT
-   [x] Image writing
-   [ ] Separate encode/decode
-   [ ] Huffman compression
-   [ ] Byte layout
-   [ ] Write own DCT routine
-   [ ] Write own Huffman routine

## References

-   [The Unreasonable Effectiveness of JPEG: A Signal Processing Approach](https://www.youtube.com/watch?v=0me3guauqOU&t=501s)
-   [JPEG - Wikipedia](https://en.wikipedia.org/wiki/JPEG#Encoding)
