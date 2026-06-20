from PIL import Image
import numpy as np

img = Image.open('/Users/emreoktem/.gemini/antigravity/brain/abbeaea4-ac89-4227-845f-a61f7afd2e45/media__1781827800228.png').convert("L")
arr = np.array(img)

# Dark pixels are less than 150
dark_mask = arr < 150

# Sum along rows (y-axis) and columns (x-axis)
row_sums = np.sum(dark_mask, axis=1)
col_sums = np.sum(dark_mask, axis=0)

# Find rows where there are dark pixels (representing the car/man/text)
active_rows = np.where(row_sums > 5)[0]
if len(active_rows) > 0:
    print(f"Active rows range: {active_rows[0]} to {active_rows[-1]}")
    
    # Let's break down where the text vs. car is.
    # We can print sums for sections
    for i in range(0, img.height, 50):
        chunk_sum = np.sum(row_sums[i:i+50])
        if chunk_sum > 0:
            print(f"Row {i}-{i+50}: sum = {chunk_sum}")

active_cols = np.where(col_sums > 5)[0]
if len(active_cols) > 0:
    print(f"Active cols range: {active_cols[0]} to {active_cols[-1]}")
