# A Voting based Salient Object Detection
A Voting based Salient Object Detection that I had coded for a PhD scholar.

The idea is simple utilizing existing methods to generate outputs of a dataset and plugging these into a Neural Network for training. Once complete, the trained model can be further utilized for SOD.

This is my first tensorflow kernel that is a small basic project. The goal of this kernel is to create a Salient Object Detection Model that is based on the saliency maps generated from different models in comparison to the Ground Truth using Neural Networks. This achieves a higher accuracy than all the chosen comparison models as we aim to extract the best parts of the saliency maps that are close to the ground truth. Once the model is trained in a Supervised fashion, it can be further used to generate the Saliency maps of other general images by the application of the chosen comparison methods which is then provided as inputs to our trained model. The following code is tested over [DUT-OMRON](http://saliencydetection.net/dut-omron/) image database. The chosen Saliency methods are: [Discriminative Region Feature Integration (DRFI)](https://people.cs.umass.edu/~hzjiang/drfi/), [Dense and Sparse Reconstruction (DSR)](ieeexplore.ieee.org/document/6751481), [Graph based Manifold Ranking (GMR)](https://ieeexplore.ieee.org/document/6619251), [Absorbing Markov Chain (MC)](https://ieeexplore.ieee.org/document/6751317), [Robust Background Detection (RBD)](https://ieeexplore.ieee.org/document/6909756/) (Papers linked).

For more details explanation of the primary python code, refer [this link](https://www.kaggle.com/madhavan93/voting-based-salient-object-detection?scriptVersionId=8175537) on Kaggle.

The images that I have used for testing and creation of the model is attached in the following [link](https://drive.google.com/open?id=13PpabXPOuAB-QLqDVQ4oqlW5ZxWDGeZC).

Feel free to comment for more details
