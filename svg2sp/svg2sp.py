from PIL import Image

#raw_image.save('ball16.png')

# Make the background transparent
image = Image.open('ball1.png')
background = Image.new('RGBA', image.size, (0, 0, 0, 0))
image = Image.alpha_composite(background, image)
image.save('ball_t.png')

raw_image = Image.open('ball1.png').resize((16,16)).quantize(colors=15)

raw_image_bytes = raw_image.tobytes()
raw_image_pallet = raw_image.getpalette()

dots = []

for b in raw_image_bytes:
    if (b == 0 or b == 1):
        dots.append("0")
    else:
        dots.append(str(b+1))

for y in range(16):
    a = ",".join(dots[y*16:y*16+16])
    print("    "+a+",")

print()

print("  0,",end="")

for i in range(15):
    r = raw_image_pallet[ i * 3 + 0 ]
    g = raw_image_pallet[ i * 3 + 1 ]
    b = raw_image_pallet[ i * 3 + 2 ]
    rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 1
    print(f"{hex(rgb555)},",end="")

print()
