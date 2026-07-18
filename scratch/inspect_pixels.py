from PIL import Image
img = Image.open('/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827988066.png')
print("Image size:", img.size)
# Print some pixels from top-left, bottom-left, top-right, bottom-right, and center
width, height = img.size
print("Top-left pixel:", img.getpixel((10, 10)))
print("Bottom-left pixel:", img.getpixel((10, height - 10)))
print("Top-right pixel:", img.getpixel((width - 10, 10)))
print("Bottom-right pixel:", img.getpixel((width - 10, height - 10)))
print("Center pixel:", img.getpixel((width // 2, height // 2)))
