# Architecture testing

In the process of finding the best architecture for this project,
I played with a number of hyper-parameters, as described in the
specifications.

I started with a baseline equal to the NN used in the lecture to classify
MNIST images: 
- 1 conv layer with 32 3x3 filters,
- 1 pooling layer with 2x2 pool size,
- 1 hidden layer with 128 neurons and 0.5 dropout

and from there, I varied one parameter at a time to see its influence in
accuracy.
The best combinations of parameters I found resulted in an testing 
accuracy of 97.8% (averaging 5 independent runs, like in all other parameter
combinations).
The winning architecture is:
- 1 conv layer with 32 5x5 filters,
- 1 conv layer with 32 4x4 filters,
- 1 conv layer with 32 3x3 filters,
- 1 pooling layer with 2x2 pool size,
- 1 hidden layer with 128 neurons and 0.1 dropout

Afterwards, I searched for inspiration in famous ConvNet architectures.
I interweaved convolutional and pooling layers with different parameters,
but no combination I tried was able to top the one above for this dataset.
