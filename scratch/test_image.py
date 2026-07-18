from PIL import Image

img = Image.open('/Users/emreoktem/Stick Bridge Game/images/gnx_car.png')
print("Dimensions:", img.size)
print("Mode:", img.mode)

# Let's count non-transparent pixels
pixels = list(img.getdata())
non_transparent = sum(1 for p in pixels if p[3] > 0)
print("Total pixels:", len(pixels))
print("Non-transparent pixels:", non_transparent)
