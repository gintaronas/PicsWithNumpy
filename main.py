import os
import sys
import configparser
import easygui
import numpy as np
from PIL import Image

# Load an image or exit, if not selected
try:
    image_path = easygui.fileopenbox(default="input/*")
    image = Image.open(image_path)
    width, height = image.size
    print(f"Original picture. Width: {width}px, Height: {height}px")
except:  # whatever happens otherwise - exit
    sys.exit()
# print(f'{image_path}')
head, tail = os.path.split(image_path)
# print(f'{tail}')
# Show the original image
image.show()

# Convert the image to a NumPy array
img_array = np.array(image)
start_row, start_col = 0, 0
end_row = height
end_col = width


#  Let's determine the number of slices to be used


def num_of_slices(width_pix: int, desired_sl_width: int):
    num_slices = width_pix // desired_sl_width
    remainder_width = width_pix % desired_sl_width
    actual_slice_width = desired_sl_width
    if remainder_width > 0:
        actual_slice_width += remainder_width // num_slices
    return num_slices, actual_slice_width


config = configparser.ConfigParser()
config.read('config.ini')
desired_slice_width = int(config['Settings']['desired_slice_width'])

slicing_v = num_of_slices(width, desired_slice_width)

num_v_slices = slicing_v[0]
slice_width = slicing_v[1]
print(f'Slicing vertically by stripes of {slice_width}px')
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
print(f'Vertically sliced and concatenated. Width: {width}px, Height: {height}px')

joined_image.show()

slicing_h = num_of_slices(height, desired_slice_width)

num_h_slices = slicing_h[0]
slice_height = slicing_h[1]
print(f'Slicing horizontally by stripes of {slice_height}px')
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
height, width, channels = joined_h_img_array.shape
print(f"Horizontally sliced and concatenated. Width: {width}px, Height: {height}px")
joined_h_image.show()

# Ensure the images have the same width. if yes, concatenate vertically

try:
    assert img_array.shape[1] == joined_img_array.shape[1] == joined_h_img_array.shape[1], "Images must have the same \
                                                                                            width to put them into one"
    total_img_array = np.concatenate((img_array, joined_img_array, joined_h_img_array), axis=0)
    total_image = Image.fromarray(total_img_array)
    total_image.show()
    output_file_name = 'output/' + 'too_many_of_' + tail
    total_image.save(output_file_name)
except AssertionError:
    print(f'Images must have the same width to put them into one.')
    # If we can't join the pictures into one due to different dimensions, let's save them separately anyway
finally:
    output_file_name_1st_split = 'output/' + 'two_of_' + tail
    joined_image.save(output_file_name_1st_split)
    output_file_name_h_split = 'output/' + 'four_times_' + tail
    joined_h_image.save(output_file_name_h_split)
