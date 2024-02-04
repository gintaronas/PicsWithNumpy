import numpy as np
from PIL import Image

# Load an image
image_path = 'cat.jpg'
image = Image.open(image_path)
width, height = image.size
print(f"Width: {width}px, Height: {height}px")

# Show the original image
image.show()

# Convert the image to a NumPy array
img_array = np.array(image)
start_row, start_col = 0, 0
end_row = height
end_col = width

num_v_slices = 320
slice_width = width // num_v_slices

slices1 = []
slices2 = []

for i in range(num_v_slices):
    start_col = i * slice_width
    end_col = (i + 1) * slice_width
    if i == 0 or i % 2:
        slices1.append(img_array[:, start_col:end_col, :])
    else:
        slices2.append(img_array[:, start_col:end_col, :])

joined_img_array1 = np.concatenate(slices1, axis=1)
joined_img_array2 = np.concatenate(slices2, axis=1)

# This is the one we will slice further by rows
joined_img_array = np.concatenate((joined_img_array1, joined_img_array2), axis=1)

joined_image1 = Image.fromarray(joined_img_array1)
joined_image2 = Image.fromarray(joined_img_array2)
joined_image = Image.fromarray(joined_img_array)

height, width, channels = joined_img_array.shape
print(f"Width: {width}px, Height: {height}px")

# Display and save the joined image
# joined_image1.show()
# joined_image2.show()
joined_image.show()

num_h_slices = 210
slice_height = height // num_h_slices

h_slices1 = []
h_slices2 = []

for i in range(num_h_slices):
    start_row = i * slice_height
    end_row = (i + 1) * slice_height
    if i == 0 or i % 2:
        h_slices1.append(joined_img_array[start_row:end_row, :, :])
    else:
        h_slices2.append(joined_img_array[start_row:end_row, :, :])

joined_h_img_array1 = np.concatenate(h_slices1, axis=0)
joined_h_img_array2 = np.concatenate(h_slices2, axis=0)
joined_h_img_array = np.concatenate((joined_h_img_array1, joined_h_img_array2), axis=0)
joined_h_image1 = Image.fromarray(joined_h_img_array1)
joined_h_image2 = Image.fromarray(joined_h_img_array2)
joined_h_image = Image.fromarray(joined_h_img_array)
# joined_h_image1.show()
# joined_h_image2.show()
height, width, channels = joined_h_img_array.shape
print(f"Width: {width}px, Height: {height}px")
joined_h_image.show()


# Ensure the images have the same width. if yes, concatenate vertically

try:
    assert img_array.shape[1] == joined_img_array.shape[1] == joined_h_img_array.shape[1], "Images must have the same \
                                                                                            width to put them into one"
    total_img_array = np.concatenate((img_array, joined_img_array, joined_h_img_array), axis=0)
    total_image = Image.fromarray(total_img_array)
    total_image.show()
    total_image.save('too_many_cats.jpg')
except AssertionError:
    joined_image.save('two_cats.jpg')
    joined_h_image.save("four_cats.jpg")
