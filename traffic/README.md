# Architecture testing

In the process of finding the best architecture for this project,
I played with a number of hyper-parameters, as described in the
specifications.
I started with a baseline equal to the NN used in the lecture to classify
MNIST images: 
- 1 conv layer with 32 3x3 filters,
- 1 pooling layer with 2x2 pool size,
- 1 hidden layer with 128 neurons,

and from there, I varied one parameter at a time to see its influence in
performance.

For each parameter variation, I ran the process 5 times and kept track of
training and testing accuracy, as well as their difference in each run.

## Dropout
### 0

Train accuracy avg:
Test accuracy avg:
Diff avg: