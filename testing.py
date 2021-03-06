# Testing the Neural Network model
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import time
from matplotlib import pyplot as plt
from skimage import io
from skimage import img_as_ubyte


# Global constants used in the testing, resizing of images and the file-names used for each image
image_row = 300
image_column = 400
filenames = []
numOfImages = 0

# Preprocessing the images of the five different approaches chosen
def preprocessImages():
    approachFolders = [
        'images/DRFI/',
        'images/DSR/',
        'images/GMR/',
        'images/MC/',
        'images/RBD/'
    ]

    global numOfImages
    global filenames

    # Calculate number of files in any one of the folder for future computations
    numOfImages = len([name for name in os.listdir(approachFolders[0]) if os.path.isfile(os.path.join(approachFolders[0], name))])

    # X contains all the images from the 5 different approach in a matrix with shape N x 5
    # N is number of images x image row size x image column size
    X = np.zeros((numOfImages*image_column*image_row, 5), dtype=np.uint8)
    cnt = 0
    # File names of images in each folder are expected to be same with an _DRFI for DRFI images and _DSR for DSR and so on.
	# Here the file names are stored after removing _DRFI from the DRFI folder images
    for filename in os.listdir(approachFolders[0]):
        filename = filename[:-9]
        filename = filename + ".png"
        filenames.append(filename)
    
    for folder in approachFolders:
        newImgs = np.empty((0, 1), dtype=np.uint8)
        for filename in os.listdir(folder):
            img = io.imread(os.path.join(folder, filename), isGray=True)
            img = img.reshape(image_row*image_column, 1)
            newImgs = np.concatenate((newImgs, img), axis=0)
        X[:, cnt] = newImgs.flatten()
        cnt = cnt + 1

    return X


# Reverse processing converts the output from the Neural Network into a Gray-scale image format that 
# corresponds to the Saliency Map generated by the Neural Network
def reverse_process_image(finalImgArr):
    outputFolder = 'images/OP/'
    global filenames

    # Reverse Normalization using Min Max Scaler with a range between 0 and 1
    scaler = MinMaxScaler()

    global numOfImages
    for cnt in range(numOfImages):

        # Splitting into image array of size 300 x 400
        currentStart = cnt * (image_row*image_column)
        currentStop = (cnt+1) * (image_row*image_column)
        current_array = finalImgArr[currentStart:currentStop, :]
        
        current_array = np.round(scaler.fit_transform(current_array), 6)
        
        finalImage = img_as_ubyte(current_array)
        finalImage = finalImage.reshape(image_row, image_column)

        io.imsave(os.path.join(outputFolder)+filenames[cnt], finalImage)


# Model Parameters
training_epochs = 100
neurons_in_hlayer = 100
learning_rate = 0.03


# Get X Values from preprocessing
# X - N x 5
X = preprocessImages()

# Splitting the data into training and testing data 
# with 80% images falling into training set and rest into testing set
# total_train_images = int(numOfImages*0.8)
# total_test_images = numOfImages - total_train_images
# slices = int(numOfImages*0.8) * image_row*image_column
# print(slices)
# X_train, X_test = np.vsplit(X, [slices])
# Y_train, Y_test = np.vsplit(Y, [slices])

# If test set is split prior to calling this method then this can be used
X_test = X
total_train_images = 0
total_test_images = numOfImages


n_samples, n_features = X_test.shape
n_classes = 1

# Input and Expected Output of the neural networks
xs = tf.placeholder("uint8", [None, n_features], name='XtoNN')
ys = tf.placeholder("float32", [None, 1], name='YfromNN')

# Hidden Layer
xs_minmax = tf.cast(tf.divide(tf.subtract(xs, tf.reduce_min(xs)),
                              tf.subtract(tf.reduce_max(xs), tf.reduce_min(xs))), tf.float32)
weightsH = tf.Variable(tf.truncated_normal([n_features, neurons_in_hlayer], mean=0,
                                     stddev=1 / np.sqrt(n_features)), name='weights1')
biasesH = tf.Variable(tf.truncated_normal([neurons_in_hlayer],mean=0, stddev=1 / np.sqrt(n_features)), name='biases1')
yValH = tf.nn.sigmoid(tf.add(tf.matmul(xs_minmax, weightsH),biasesH), name='activationLayer1')

# Output Layer
WeightsO = tf.Variable(tf.truncated_normal([neurons_in_hlayer, n_classes], mean=0, stddev = 1/np.sqrt(n_features)),
                                           name='weightsOut')
biasesO = tf.Variable(tf.truncated_normal([n_classes], mean=0, stddev=1 / np.sqrt(n_features)), name='biasesOut')
yPred = tf.cast(tf.add(tf.matmul(yValH, WeightsO), biasesO), dtype=tf.float32, name='yOutput')

# Cost function
cost = tf.reduce_mean(tf.square(yPred-ys, name='cost'))

# Optimizer
train = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

startTime = time.time()
with tf.Session() as sess:
    saver = tf.train.Saver()
	# Restoring the model saved from Training phase
    saver.restore(sess, os.path.dirname(os.path.realpath(__file__)) + '/model/model_save2.ckpt')

    # Each test image is accessed and used in the trained Nueral Network to generate output
    y_final_predict = np.empty((0, 1), np.float32)
    for i in range(numOfImages):
        current_start = i * (image_row * image_column)
        current_stop = (i + 1) * (image_row * image_column)
        
        current_value = sess.run(yPred, feed_dict={xs: X_test[current_start:current_stop, :].reshape(image_column * image_row,
		                                                                                        n_features)})
        y_final_predict = np.append(y_final_predict, current_value)
    
    timeTaken = time.time() - startTime
    print('Time Taken: ', timeTaken)
    params_file = open("testing_params_file.txt", "w+")
    params_file.write("Time taken for testing per image in seconds %.4f\n" %(timeTaken/numOfImages))
    params_file.close()
	
    y_final_predict = y_final_predict.reshape((image_column*image_row*numOfImages, 1))
    
	# Final Reverse processing converts the output of the Neural Network into a Gray-scale image
    reverse_process_image(y_final_predict)