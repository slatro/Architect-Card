from PIL import Image

img_path = '/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827988066.png'
img = Image.open(img_path).convert("RGBA")
width, height = img.size

# Let's find columns and rows with significant opacity (> 10 alpha, and count > 2 pixels)
row_counts = [sum(1 for x in range(width) if img.getpixel((x, y))[3] > 10) for y in range(height)]
col_counts = [sum(1 for y in range(height) if img.getpixel((x, y))[3] > 10) for x in range(width)]

active_rows = [y for y, c in enumerate(row_counts) if c > 2]
active_cols = [x for x, c in enumerate(col_counts) if c > 2]

if active_rows and active_cols:
    min_y, max_y = active_rows[0], active_rows[-1]
    min_x, max_x = active_cols[0], active_cols[-1]
    print(f"Cropping box: x={min_x}..{max_x}, y={min_y}..{max_y}")
    
    # Crop the image exactly to these bounds
    cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    print("New cropped size:", cropped.size)
    cropped.save('/Users/emreoktem/Stick Bridge Game/images/gnx_car.png', "PNG")
else:
    print("Could not find active pixels.")
