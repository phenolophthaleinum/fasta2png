from PIL import Image
import glob
import os
import argparse


def make_textures(pattern):
    # TGA2PNG
    # path = os.path.dirname(pattern)
    # for file in glob.glob(f"{pattern}"):
    #     print(file)
    #     tga_img = Image.open(file)
    #     tga_img.save(f"{path}\{os.path.basename(file).split('.')[0]}.png")

    # create maskmap
    r_ch = Image.open(f"{pattern.split('*')[0]}_bz2.png").convert("L")
    g_ch = Image.open(f"{pattern.split('*')[0]}_lz4.png").convert("L")
    b_ch = Image.open(f"{pattern.split('*')[0]}_ppm.png").convert("L")
    a_ch = Image.open(f"{pattern.split('*')[0]}_zstd.png").convert("L")

    maskmap = Image.merge("RGBA", (r_ch, g_ch, b_ch, a_ch))
    maskmap.save(f"{pattern.split('*')[0]}_maskmap.png")
    print(f"{pattern.split('*')[0]}_maskmap.png")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automated textures generation for Unity HDRP")
    parser.add_argument('-i', '--input', required=True,
                        help="Files to open (use regexp), e.g. rock002*.tga")
    args = parser.parse_args()

    make_textures(args.input)
