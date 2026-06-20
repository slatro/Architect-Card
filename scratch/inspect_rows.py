from PIL import Image

img = Image.open('/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827988066.png').convert("RGBA")
width, height = img.size

# Let's count how many non-transparent pixels there are in each row
row_counts = []
for y in range(height):
    count = 0
    for x in range(width):
        r, g, b, a = img.getpixel((x, y))
        # If alpha is greater than 10, count it
        if a > 10:
            count += 1
    row_counts.append(count)

# Let's print rows that have a significant number of non-transparent pixels (e.g. > 5 pixels)
active_rows = [y for y, c in enumerate(row_counts) if c > 5]
if active_rows:
    print(f"Active rows range (with >5 pixels): {active_rows[0]} to {active_rows[-1]}")
    
    # Print a few row counts around the boundaries
    for y in active_rows[:15]:
        print(f"Row {y}: {row_counts[y]} pixels")
    print("...")
    for y in active_rows[-15:]:
        print(f"Row {y}: {row_counts[y]} pixels")
else:
    print("No active rows found.")
