import argparse

from PIL import Image

def convert_png_to_sp(png_file,out_format,out_file,size=(16,16)):

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

    # generate sprite pattern array data
    pattern_array = []
    for i,b in enumerate(color15_image_bytes):
        if (alpha[i] == 0):
            pattern_array.append(0)
        else:
            pattern_array.append(b+1)

    if out_format == "b":

        # output pattern array data
        print("/* sprite data */")
        for y in range(16):
            s = [str(n) for n in pattern_array[ y * 16 : (y+1) * 16 ]]
            print(",".join(s)+",")
    
    else:

        # convert dot data to raw pattern data
        pattern_data = [ 0 ] * 128
        for y in range(8):
            for x in range(4):
                pattern_data[ 0x00 + y*4 + x ] = ( pattern_array[ (y+0)*16 + (x+0)*2 ] << 4 ) | ( pattern_array[ (y+0)*16 + (x+0)*2 + 1])
                pattern_data[ 0x20 + y*4 + x ] = ( pattern_array[ (y+8)*16 + (x+0)*2 ] << 4 ) | ( pattern_array[ (y+8)*16 + (x+0)*2 + 1])
                pattern_data[ 0x40 + y*4 + x ] = ( pattern_array[ (y+0)*16 + (x+4)*2 ] << 4 ) | ( pattern_array[ (y+0)*16 + (x+4)*2 + 1])
                pattern_data[ 0x60 + y*4 + x ] = ( pattern_array[ (y+8)*16 + (x+4)*2 ] << 4 ) | ( pattern_array[ (y+8)*16 + (x+4)*2 + 1])

        # output raw pattern data
        print("/* sprite data */")
        for y in range(8):
            tuples = [ tuple( pattern_data[ y * 16 : (y+1) * 16 ]) for i in range(0, 16, 2)]
            s = [ '0x' + format(t[0],'02x') + format(t[1],'02x') for t in tuples ]
            print(",".join(s)+",")



    # generate palette data
    palette_data = []
    palette_data.append(0)      # palette 0 = transparent code
    for i in range(15):
        r = color15_image_pallet[ i * 3 + 0 ]
        g = color15_image_pallet[ i * 3 + 1 ]
        b = color15_image_pallet[ i * 3 + 2 ]
        rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 1
        palette_data.append(rgb555)

    # output palette data
    print()
    print("/* palette data */")
    s = [ '0x' + format(p,'04x') for p in palette_data ]
    print(",".join(s)+",")
    print()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile",help="input PNG file")
    parser.add_argument("-f","--format",help="output format (b:X-BASIC, r:raw)",default="b")
    parser.add_argument("-o","--outfile",help="output file")
    parser.add_argument("-x","--width",help="sprite width (default:16)",type=int,default=16)
    parser.add_argument("-y","--height",help="sprite height (default:16)",type=int,default=16)

    args = parser.parse_args()

    convert_png_to_sp(args.infile,args.format,args.outfile,(args.width,args.height))


if __name__ == "__main__":
    main()