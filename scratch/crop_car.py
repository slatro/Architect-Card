from PIL import Image

# Load the clean car image uploaded by user
img_path = '/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827988066.png'
img = Image.open(img_path).convert("RGBA")

# Convert to numpy array-like list of pixels
data = img.getdata()
new_data = []

# Since the background is very clean white/light-gray, let's use a threshold of 200.
# Any pixel where R, G, B are all > 200 is considered background and made fully transparent.
threshold = 200

for item in data:
    r, g, b, a = item
    if r > threshold and g > threshold and b > threshold:
        new_data.append((0, 0, 0, 0)) # transparent
    else:
        new_data.append((r, g, b, a))

img.putdata(new_data)

# Crop to bounding box of non-transparent pixels
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)
    print("New cropped bounding box size:", img.size)

img.save('/Users/emreoktem/Stick Bridge Game/images/gnx_car.png', "PNG")
print("Saved cropped transparent image.")
