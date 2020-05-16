import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
import os
import matplotlib.pyplot as plt


def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Parameters configured in SplitImageDataset 
    train_dir = sid.train_dir
    val_dir = sid.val_dir
    test_dir = sid.test_dir
    ############################################
    # Parameters configured in ImageGenerator 
    color_mode= ig.color_mode
    img_height = ig.img_height
    img_width = ig.img_width  
    class_mode= ig.class_mode
    batch_size = ig.batch_size
    epochs = ig.epochs                                   
    shuffle = ig.shuffle                                                             
    seed = ig.seed
    # Parameters for test dataset 
    test_batch_size = 1

    ########################################
    # ImageDataGenerator
    ## Read images from the disk.
    ## Decode contents of these images and convert it into proper grid format as per their RGB content.
    ## Convert them into floating point tensors.
    ## Rescale the tensors from values between 0 and 255 to values between 0 and 1.
    train_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    val_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    test_image_generator = ImageDataGenerator(rescale=1./255)
    
    # Generate batches of tensor image data with real-time data augmentation.
    # flow_from_directory: load images from directory, rescale and resize
    train_data_gen = train_image_generator.flow_from_directory(directory = train_dir,
                                                               target_size =(img_height, img_width),
                                                               color_mode = color_mode,
                                                               batch_size = batch_size,                                                       
                                                               shuffle = shuffle,
                                                               class_mode = class_mode,
                                                               seed=seed
                                                               ) 
    val_data_gen = val_image_generator.flow_from_directory(directory = val_dir,
                                                               target_size =(img_height, img_width),
                                                               color_mode = color_mode,
                                                               batch_size = batch_size,                                                       
                                                               shuffle = shuffle,
                                                               class_mode = class_mode,
                                                               seed=seed
                                                               )  
    test_data_gen = test_image_generator.flow_from_directory(directory = test_dir,
                                                            target_size =(img_height, img_width),
                                                            color_mode = color_mode,
                                                            batch_size = test_batch_size,                                                       
                                                            shuffle = False,
                                                            class_mode = None,
                                                            seed=seed
                                                            )  
    # Visualize training images
    ## The next function returns a batch from the dataset. 
    ## The return value of next function is in form of (x_train, y_train) where x_train is training features and y_train, its labels. 
    ## Discard the labels to only visualize the training images.
    # delete corrupt image:
    try:
        os.remove(os.path.join(train_dir, "Viburnum_opulus","Viburnum_opulus_1897827000.jpg"))
    except:
        pass
    sample_training_images, _ = next(train_data_gen)
    plotImages(sample_training_images[:5])
