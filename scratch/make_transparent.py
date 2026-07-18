from PIL import Image

# Source is the clean car image uploaded by user
img_path = '/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827988066.png'
img = Image.open(img_path).convert("RGBA")

# Convert white/near-white pixels to fully transparent
data = img.getdata()
new_data = []

threshold = 240

for item in data:
    r, g, b, a = item
    if r > threshold and g > threshold and b > threshold:
        new_data.append((0, 0, 0, 0)) # Fully transparent
    else:
        new_data.append((r, g, b, a))

img.putdata(new_data)

# Let's crop the image to the actual bounding box of the car (non-transparent pixels) to make positioning cleaner
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

# Save to destination
img.save('/Users/emreoktem/Stick Bridge Game/images/gnx_car.png', "PNG")
print("Successfully generated transparent car png and cropped bounding box.")
