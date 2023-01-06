import argparse

from PIL import Image

def convert_png_to_sp(png_file,out_file,basic_format,size=(16,16),aspect=None):

  # resize
  raw_image = Image.open(png_file)
  if aspect:
    aspect_size = ( raw_image.width * 2 // 3, raw_image.height )
    raw_image = raw_image.resize(aspect_size)

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

  # how many 16x16 patterns do we need?
  patterns_x = ( size[0] - 1 ) // 16 + 1
  patterns_y = ( size[1] - 1 ) // 16 + 1

  # output lines
  output_lines = []

  if basic_format is False:
    output_lines.append("")
    output_lines.append(f"unsigned short sp_pattern_data[] = {{")

  # generate patterns by 16x16
  for py in range(patterns_y):

    for px in range(patterns_x):

      pattern_id = py * patterns_x + px

      width = size[0]
      ofs = py * width * 16 + px * 16

      if basic_format:

        output_lines.append("")
        output_lines.append(f"/* sprite pattern data {pattern_id} */")
        output_lines.append(f"unsigned char sp_pattern_data_{pattern_id}[] = {{")

        # output pattern array data
        for y in range(16):
          s = [str(n) for n in pattern_array[ ofs + y * width : ofs + y * width + 16 ]]
          output_lines.append("    " + ",".join(s) + ",")

        output_lines.append("};")

      else:

        # convert dot data to raw pattern data
        pattern_data = [ 0 ] * 128
        for y in range(8):
          for x in range(4):
            pattern_data[ 0x00 + y*4 + x ] = ( pattern_array[ ofs + (y+0) * width + (x+0)*2 ] << 4 ) | ( pattern_array[ ofs + (y+0) * width + (x+0)*2 + 1])
            pattern_data[ 0x20 + y*4 + x ] = ( pattern_array[ ofs + (y+8) * width + (x+0)*2 ] << 4 ) | ( pattern_array[ ofs + (y+8) * width + (x+0)*2 + 1])
            pattern_data[ 0x40 + y*4 + x ] = ( pattern_array[ ofs + (y+0) * width + (x+4)*2 ] << 4 ) | ( pattern_array[ ofs + (y+0) * width + (x+4)*2 + 1])
            pattern_data[ 0x60 + y*4 + x ] = ( pattern_array[ ofs + (y+8) * width + (x+4)*2 ] << 4 ) | ( pattern_array[ ofs + (y+8) * width + (x+4)*2 + 1])

          # output raw pattern data
          output_lines.append("")
          output_lines.append(f"    /* sprite pattern data {pattern_id} */")
          for y in range(8):
            tuples = [ tuple( pattern_data[ y * 16 + x * 2 : y * 16 + x * 2 + 2 ]) for x in range(8)]
            s = [ '0x' + format(t[0],'02x') + format(t[1],'02x') for t in tuples ]
            output_lines.append("    " + ",".join(s) + ",")

  if basic_format is False:
    output_lines.append("};")

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
  output_lines.append("")
  output_lines.append("/* palette data */")
  output_lines.append("unsigned short sp_palette_data[] = {")
  s = [ '0x' + format(p,'04x') for p in palette_data ]
  output_lines.append("    " + ",".join(s) + ",")
  output_lines.append("};")
  output_lines.append("")

  # output to file or stdout
  if out_file == None:
    for l in output_lines:
      print(l)
  else:
    with open(out_file, "w") as f:
      for l in output_lines:
        f.write(l+"\n")

def convert_png_to_dump(png_file,out_file):

  # open raw image
  raw_image = Image.open(png_file).convert("RGB")
  raw_image_bytes = raw_image.tobytes()

  # output lines
  output_lines = []
  output_lines.append("")
  output_lines.append(f"unsigned short dump_data[] = {{")

  # dump data
  pixels = []
  for i,b in enumerate(raw_image_bytes):
    if ( i % 3 ) == 2:
      r = raw_image_bytes [ i - 2 ]
      g = raw_image_bytes [ i - 1 ]
      b = raw_image_bytes [ i - 0 ]
      rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 0
      pixels.append('0x' + format(rgb555, '04x'))
      if ( i % 36 ) == 35:
        output_lines.append(",".join(pixels) + ",")
        pixels = []

  if len(pixels) > 0:
    output_lines.append("    " + ",".join(pixels) + ",")
    pixels = []    

  output_lines.append("};")

  # output to file or stdout
  if out_file == None:
    for l in output_lines:
      print(l)
  else:
    with open(out_file, "w") as f:
      for l in output_lines:
        f.write(l+"\n")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile",help="input PNG file")
    parser.add_argument("-o","--outfile",help="output file")
    parser.add_argument("-b","--basic",help="output in X-BASIC like format",action='store_true',default=False)
    parser.add_argument("-x","--width",help="sprite width (default:16)",type=int,default=16)
    parser.add_argument("-y","--height",help="sprite height (default:16)",type=int,default=16)
    parser.add_argument("-a","--aspect",help="resize source image to 2:3",action='store_true',default=False)
    parser.add_argument("-d","--dump",help="output in GVRAM dump format",action='store_true',default=False)

    args = parser.parse_args()

    if args.dump:
      convert_png_to_dump(args.infile,args.outfile)
    else:
      convert_png_to_sp(args.infile,args.outfile,args.basic,(args.width,args.height),args.aspect)


if __name__ == "__main__":
    main()
