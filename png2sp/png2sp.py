import argparse

from PIL import Image

def convert_png_to_sp(png_file,out_file,size=(16,16)):

    # resize
    raw_image = Image.open(png_file)
    resize_image = raw_image.convert('RGBA').resize(size)
    resize_image_bytes = resize_image.tobytes()

    # extract alpha channel
    alpha = []
    for i,b in enumerate(resize_image_bytes):
        if (i % 4) == 3:
            if (b < 32):            # transparent alpha threshould
                p = 0
            else:
                p = -1
            alpha.append(p)

    # color reduction
    color15_image = resize_image.quantize(colors=15)
    color15_image_bytes = color15_image.tobytes()
    color15_image_pallet = color15_image.getpalette()

    # generate sprite dot data
    sprite_dots = []
    for i,b in enumerate(color15_image_bytes):
        if (alpha[i] == 0):
            sprite_dots.append("0")
        else:
            sprite_dots.append(str(b+1))

    # output sprite dot data
    for y in range(16):
        a = ",".join(sprite_dots[y*16:y*16+16])
        print("    "+a+",")

    print()

    print("  0,",end="")

    for i in range(15):
        r = color15_image_pallet[ i * 3 + 0 ]
        g = color15_image_pallet[ i * 3 + 1 ]
        b = color15_image_pallet[ i * 3 + 2 ]
        rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 1
        print(f"{hex(rgb555)},",end="")

    print()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile",help="input PNG file")
    parser.add_argument("-o","--outfile",help="output file")
    parser.add_argument("-x","--width",help="sprite width (default:16)",type=int,default=16)
    parser.add_argument("-y","--height",help="sprite height (default:16)",type=int,default=16)

    args = parser.parse_args()

    convert_png_to_sp(args.infile,args.outfile,(args.width,args.height))


if __name__ == "__main__":
    main()