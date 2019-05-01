# Training the Neural Network model
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

    groundTruthFolder = 'images/GTRUTH/'
    # Y contains the ground truth values in row vector with shape N x 1
    # N is number of images x image row size x image column size
    Y = np.empty((0, 1), dtype=np.uint8)

    # First we calculate Y so as to get the number of images for training and testing
    for filename in os.listdir(groundTruthFolder):
        filenames.append(filename)
        img = io.imread(os.path.join(groundTruthFolder, filename), isGray=True)
        img = img.reshape(image_row, image_column)
        if img is not None:
            Y = np.append(Y, img.reshape((image_row*image_column, 1)), axis=0)
            numOfImages = numOfImages + 1

    # X contains all the images from the 5 different approach in a matrix with shape N x 5
    X = np.zeros((numOfImages*image_column*image_row, 5), dtype=np.uint8)
    cnt = 0
    for folder in approachFolders:
        newImgs = np.empty((0, 1), dtype=np.uint8)
        for filename in os.listdir(folder):
            img = io.imread(os.path.join(folder, filename), isGray=True)
            img = img.reshape(image_row*image_column, 1)
            newImgs = np.concatenate((newImgs, img), axis=0)
        X[:, cnt] = newImgs.flatten()
        cnt = cnt + 1

    return X, Y


# Reverse processing converts the output from the Neural Network into a Gray-scale image format that 
# corresponds to the Saliency Map generated by the Neural Network
def reverseProcessImage(Y, finalImgArr):
    outputFolder = 'images/OP/'
    global filenames

    # Reverse Normalization using Min Max Scaling with range between 0 and 1
    scaler = MinMaxScaler()
    scaler.fit_transform(Y)

    global numOfImages
	# Converts the output from the Neural Network into a Gray-scale images
    for cnt in range(numOfImages):

        # Splitting the data into images of size 300x400
        currentStart = cnt * (image_row*image_column)
        currentStop = (cnt+1) * (image_row*image_column)
        currentArray = finalImgArr[currentStart:currentStop, :]

        currentArray = np.round(scaler.fit_transform(currentArray), 6)
        
        # Final image is the saliency output generated from the Neural Network
        finalImage = img_as_ubyte(currentArray)
        finalImage = finalImage.reshape(image_row, image_column)

        io.imsave(os.path.join(outputFolder)+filenames[cnt], finalImage)


# Model Parameters
training_epochs = 150
neurons_in_hlayer = 100
learning_rate = 0.03

# Get X and y Values from preprocessing
# X - N x 5, Y - N x 1
X, Y = preprocessImages()

# Splitting the data into training and testing data 
# with 80% images falling into training set and rest into testing set
# total_train_images = int(numOfImages*0.8)
# total_test_images = numOfImages - total_train_images
# slices = int(numOfImages*0.8) * image_row*image_column
# print(slices)
# X_train, X_test = np.vsplit(X, [slices])
# Y_train, Y_test = np.vsplit(Y, [slices])

# If training is split prior to calling this method then this can be used
X_train = X
Y_train = Y
total_train_images = numOfImages
total_test_images = 0

# Scaling using Min Max Scaling with range between 0 and 1
scaler = MinMaxScaler()
Y_train = scaler.fit_transform(Y_train)

n_samples, n_features = X_train.shape
# number of classes in the output is set to 1 since we use Regression to predict the saliency values
n_classes = 1

# Input and Expected Output of the neural networks
xs = tf.placeholder("uint8", [None, n_features], name='XtoNN')
ys = tf.placeholder("float32", [None, 1], name='YfromNN')

# Hidden Layer uses Min-Max normalized batch inputs and uses a Sigmoid activation function at the hidden layer
xs_minmax = tf.cast(tf.divide(tf.subtract(xs, tf.reduce_min(xs)),
                              tf.subtract(tf.reduce_max(xs), tf.reduce_min(xs))), tf.float32)
weightsH = tf.Variable(tf.truncated_normal([n_features, neurons_in_hlayer], mean=0,
                                     stddev=1 / np.sqrt(n_features)), name='weights1')
biasesH = tf.Variable(tf.truncated_normal([neurons_in_hlayer],mean=0, stddev=1 / np.sqrt(n_features)), name='biases1')
yValH = tf.nn.sigmoid(tf.add(tf.matmul(xs_minmax, weightsH),biasesH), name='activationLayer1')

# Output Layer is generated using a direct matrix multiplication of weights and the output layer of previous hidden layer
WeightsO = tf.Variable(tf.truncated_normal([neurons_in_hlayer, n_classes], mean=0, stddev = 1/np.sqrt(n_features)),
                                           name='weightsOut')
biasesO = tf.Variable(tf.truncated_normal([n_classes], mean=0, stddev=1 / np.sqrt(n_features)), name='biasesOut')
yPred = tf.cast(tf.add(tf.matmul(yValH, WeightsO), biasesO), dtype=tf.float32, name='yOutput')

# Cost function Mean Squared error from the output layer to ground truth
cost = tf.reduce_mean(tf.square(yPred-ys, name='cost'))

# Optimizer we use Gradient Descent to minimize the cost function define above
train = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

startTime = time.time()
# Tensorflow Session begins
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    saver = tf.train.Saver()
    cost_list = []
    for i in range(training_epochs):
        currentEpochCost = 0
        for j in range(total_train_images):
            # Run Neural Network
            current_start = j * (image_row * image_column)
            current_stop = (j + 1) * (image_row * image_column)
            currentEpochCost, trainer = sess.run([cost, train], feed_dict={xs: X_train[current_start:current_stop, :]
                     .reshape(image_column*image_row, n_features),
                                                   ys: Y_train[current_start:current_stop]
                     .reshape(image_column*image_row, n_classes)})

        cost_list.append(currentEpochCost)
        print('Epoch ', (i+1), ': Final Image Cost = ', currentEpochCost)

    timeTaken = time.time() - startTime
    print('Time Taken in seconds: ', timeTaken)
    params_file = open("training_params_file.txt", "w+")
    params_file.write("Images resized to %d x %d\n" %(image_row, image_column))
    params_file.write("Total number of images %d\n" %(numOfImages))
    params_file.write("Total number of training epochs %d\n" %(training_epochs))
    params_file.write("Total number of neurons in the hidden layer is %d\n" %(neurons_in_hlayer))
    params_file.write("Learning rate used for the training %.4f\n" %(learning_rate))
    params_file.write("Total time taken in seconds %.4f\n" %(timeTaken))
    params_file.write("Time taken per image in seconds %.4f\n" %(timeTaken/numOfImages))
    params_file.close()

    # Save Model
    save_path = saver.save(sess, os.path.dirname(os.path.realpath(__file__)) + '\model\model_save2.ckpt')
    print('Model saved at ', save_path)