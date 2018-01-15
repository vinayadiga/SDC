import cv2 # computer vision library
import helpers # helper functions

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # for loading in images

%matplotlib inline

IMAGE_DIR_TRAINING = "traffic_light_images/training/"
IMAGE_DIR_TEST = "traffic_light_images/test/"

# Load training data
IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAINING)

# The first image in IMAGE_LIST
selected_image = IMAGE_LIST[0][0]
plt.imshow(selected_image)
print(selected_image.shape)
print(IMAGE_LIST[0][1])

# This function should take in an RGB image and return a new, standardized version
def standardize_input(image):
    
    ## TODO: Resize image and pre-process so that all "standard" images are the same size  
    standard_im = np.copy(image)
    dimension = (32, 32)
    resized_im = cv2.resize(standard_im, dimension, interpolation = cv2.INTER_AREA)
    blur = cv2.GaussianBlur(resized_im,(5,5), 0)
    # Sharpen the image - https://en.wikipedia.org/wiki/Kernel_(image_processing)
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    standardized_im = cv2.filter2D(blur, -1, kernel)
    return standardized_im


## Given a label - "red", "green", or "yellow" - return a one-hot encoded label
def one_hot_encode(label):
    
    ## TODO: Create a one-hot encoded label that works for all classes of traffic lights
    one_hot_encoded = [] 
    if label == "red":
        one_hot_encoded = [1, 0, 0]
    elif label == "yellow":
        one_hot_encoded = [0, 1, 0]
    elif label == "green":
        one_hot_encoded = [0, 0, 1]
    else:
        one_hot_encoded = [0, 0, 0]
    
    return one_hot_encoded


def standardize(image_list):
    
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)

        # One-hot encode the label
        one_hot_label = one_hot_encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, one_hot_label))
        
    return standard_list

# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)

# Convert and image to HSV colorspace
# Visualize the individual color channels

image_num = 100
test_im = STANDARDIZED_LIST[image_num][0]
test_label = STANDARDIZED_LIST[image_num][1]

# Convert to HSV
hsv = cv2.cvtColor(test_im, cv2.COLOR_RGB2HSV)

# Print image label
print('Label [red, yellow, green]: ' + str(test_label))

# HSV channels
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

# Plot the original image and the three channels
f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20,10))
ax1.set_title('Standardized image')
ax1.imshow(test_im)
ax2.set_title('H channel')
ax2.imshow(h, cmap='gray')
ax3.set_title('S channel')
ax3.imshow(s, cmap='gray')
ax4.set_title('V channel')
ax4.imshow(v, cmap='gray')

## This feature should use HSV colorspace values
def create_feature(rgb_image):
    
    ## TODO: Convert image to HSV color space
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    ## TODO: Create and return a feature value and/or vector
    feature = []
    #red color
    lower_red_1 = np.array([0,80,60]) 
    upper_red_1 = np.array([10,255,255])
    lower_red_2 = np.array([160,80,60]) 
    upper_red_2 = np.array([180,255,255])
    roi = hsv[0:11, 5:25]
    mask_red_1 = cv2.inRange(roi, lower_red_1, upper_red_1)
    mask_red_2 = cv2.inRange(roi, lower_red_2, upper_red_2)
    mask_red = mask_red_1 | mask_red_2
    image = mask_red
    masked_image = np.copy(roi)
    masked_image[image == 0] = [0, 0, 0]
    mean_red = masked_image.mean()
    
    #yellow color
    lower_yellow = np.array([10,50,90]) 
    upper_yellow = np.array([45,255,255])
    roi = hsv[12:22, 5:25]
    mask_yellow = cv2.inRange(roi, lower_yellow, upper_yellow)
    image = mask_yellow
    masked_image = np.copy(roi)
    masked_image[image == 0] = [0, 0, 0]
    mean_yellow = masked_image.mean()
    
    #green color
    lower_green = np.array([50,30,60]) 
    upper_green = np.array([96,255,255])
    roi = hsv[22:32, 5:25]
    mask_green = cv2.inRange(roi, lower_green, upper_green)
    image = mask_green
    masked_image = np.copy(roi)
    masked_image[image == 0] = [0, 0, 0]
    mean_green = masked_image.mean()
    
    return mean_red, mean_yellow, mean_green


# This function should take in RGB image input
# Analyze that image using your feature creation code and output a one-hot encoded label
def estimate_label(rgb_image):
    
    ## TODO: Extract feature(s) from the RGB image and use those features to
    ## classify the image and output a one-hot encoded label
    predicted_label = ""
    mean_red, mean_yellow, mean_green = create_feature(rgb_image)
    if mean_red >= mean_yellow:
        if mean_red >= mean_green:
            predicted_label = "red"
        else:
            predicted_label = "green"
    else:
        if mean_yellow >= mean_green:
            predicted_label = "yellow"
        else:
            predicted_label = "green"
    return one_hot_encode(predicted_label)  


# Constructs a list of misclassified images given a list of test images and their labels
# This will throw an AssertionError if labels are not standardized (one-hot encoded)
def get_misclassified_images(test_images):
    # Track misclassified images by placing them into a list
    misclassified_images_labels = []

    # Iterate through all the test images
    # Classify each image and compare to the true label
    for image in test_images:

        # Get true data
        im = image[0]
        true_label = image[1]
        assert(len(true_label) == 3), "The true_label is not the expected length (3)."

        # Get predicted label from your classifier
        predicted_label = estimate_label(im)
        assert(len(predicted_label) == 3), "The predicted_label is not the expected length (3)."

        # Compare true and predicted labels 
        if(predicted_label != true_label):
            # If these labels are not equal, the image has been misclassified
            misclassified_images_labels.append((im, predicted_label, true_label))
            
    # Return the list of misclassified [image, predicted_label, true_label] values
    return misclassified_images_labels


# Find all misclassified images in a given test set
MISCLASSIFIED = get_misclassified_images(STANDARDIZED_TEST_LIST)

# Accuracy calculations
total = len(STANDARDIZED_TEST_LIST)
num_correct = total - len(MISCLASSIFIED)
accuracy = num_correct/total

print('Accuracy: ' + str(accuracy))
print("Number of misclassified images = " + str(len(MISCLASSIFIED)) +' out of '+ str(total))
