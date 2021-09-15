#!/usr/bin/env python
# coding: utf-8

# # A2: NeuralNetwork Class

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Requirements" data-toc-modified-id="Requirements-1">Requirements</a></span></li><li><span><a href="#Code-for-NeuralNetwork-Class" data-toc-modified-id="Code-for-NeuralNetwork-Class-2">Code for <code>NeuralNetwork</code> Class</a></span></li><li><span><a href="#Example-Results" data-toc-modified-id="Example-Results-3">Example Results</a></span></li><li><span><a href="#Application-to-Boston-Housing-Data" data-toc-modified-id="Application-to-Boston-Housing-Data-4">Application to Boston Housing Data</a></span></li></ul></div>

# ## Requirements

# In this assignment, you will complete the implementation of the `NeuralNetwork` class, starting with the code included in the next code cell.  Your implementation must meet the requirements described in the doc-strings.
# 
# Then apply your `NeuralNetwork` class to the problem of predicting the value of houses in Boston as described below.

# ## Code for `NeuralNetwork` Class

# In[1]:


get_ipython().run_cell_magic('writefile', 'neuralnetwork.py', '\nimport numpy as np\nimport optimizers as opt\n\n\nclass NeuralNetwork():\n    """\n    A class that represents a neural network for nonlinear regression\n\n    Attributes\n    ----------\n    n_inputs : int\n        The number of values in each sample\n    n_hidden_units_by_layers: list of ints, or empty\n        The number of units in each hidden layer.\n        Its length specifies the number of hidden layers.\n    n_outputs: int\n        The number of units in output layer\n    all_weights : one-dimensional numpy array\n        Contains all weights of the network as a vector\n    Ws : list of two-dimensional numpy arrays\n        Contains matrices of weights in each layer,\n        as views into all_weights\n    all_gradients : one-dimensional numpy array\n        Contains all gradients of mean square error with\n        respect to each weight in the network as a vector\n    Grads : list of two-dimensional numpy arrays\n        Contains matrices of gradients weights in each layer,\n        as views into all_gradients\n    total_epochs : int\n        Total number of epochs trained so far\n    error_trace : list\n        Mean square error (standardized) after each epoch\n    X_means : one-dimensional numpy array\n        Means of the components, or features, across samples\n    X_stds : one-dimensional numpy array\n        Standard deviations of the components, or features, across samples\n    T_means : one-dimensional numpy array\n        Means of the components of the targets, across samples\n    T_stds : one-dimensional numpy array\n        Standard deviations of the components of the targets, across samples\n        \n    Methods\n    -------\n    make_weights_and_views(shapes)\n        Creates all initial weights and views for each layer\n\n    train(X, T, n_epochs, method=\'sgd\', learning_rate=None, verbose=True)\n        Trains the network using samples by rows in X and T\n\n    use(X)\n        Applies network to inputs X and returns network\'s output\n    """\n\n    def __init__(self, n_inputs, n_hidden_units_by_layers, n_outputs):\n        """Creates a neural network with the given structure\n\n        Parameters\n        ----------\n        n_inputs : int\n            The number of values in each sample\n        n_hidden_units_by_layers : list of ints, or empty\n            The number of units in each hidden layer.\n            Its length specifies the number of hidden layers.\n        n_outputs : int\n            The number of units in output layer\n\n        Returns\n        -------\n        NeuralNetwork object\n        """\n\n        # Assign attribute values. Set self.X_means to None to indicate\n        # that standardization parameters have not been calculated.\n        # ....\n        self.n_inputs = n_inputs\n        self.n_hidden_units_by_layers = n_hidden_units_by_layers\n        self.n_outputs = n_outputs\n        self.total_epochs = 0\n        self.error_trace = []\n        self.X_means = None\n        self.X_stds = None\n        self.T_means = None\n        self.T_stds = None\n        \n        # Build list of shapes for weight matrices in each layer\n        # ...\n        shapes = []\n        if n_hidden_units_by_layers:\n            for n in range(len(n_hidden_units_by_layers)):\n                if n == 0:\n                    shapes.append((1 + n_inputs, n_hidden_units_by_layers[n]))\n                else:\n                    shapes.append((1 + n_hidden_units_by_layers[n-1], n_hidden_units_by_layers[n]))\n\n            shapes.append((1 + n_hidden_units_by_layers[len(n_hidden_units_by_layers)-1], n_outputs))\n        else:\n            # no hidden layers, i.e. empty list passed in for n_hidden_units_by_layers\n            shapes.append((1 + n_inputs, n_outputs))\n        \n        # Call make_weights_and_views to create all_weights and Ws\n        # ...\n        self.all_weights, self.Ws = self.make_weights_and_views(shapes)\n        \n        # Call make_weights_and_views to create all_gradients and Grads\n        # ...\n        self.all_gradients, self.Grads = self.make_weights_and_views(shapes)\n\n\n    def make_weights_and_views(self, shapes):\n        """Creates vector of all weights and views for each layer\n\n        Parameters\n        ----------\n        shapes : list of pairs of ints\n            Each pair is number of rows and columns of weights in each layer\n\n        Returns\n        -------\n        Vector of all weights, and list of views into this vector for each layer\n        """\n\n        # Create one-dimensional numpy array of all weights with random initial values\n        #  ...\n        array_size = 0\n        for shape in shapes:\n            array_size += (shape[0] * shape[1])\n        all_weights = np.random.uniform(-1, 1, size=array_size)\n        \n        index = 0\n        new_index = 0\n        for shape in shapes:\n            new_index += (shape[0] * shape[1])\n            all_weights[index:new_index] = all_weights[index:new_index] / shape[0]\n            index = new_index\n        # Build list of views by reshaping corresponding elements\n        # from vector of all weights into correct shape for each layer.        \n        # ...\n        #TODO make sure division makes sense / np.sqrt(shapes[0]\n        \n        views = []\n        index = 0\n        new_index = 0\n        for shape in shapes:\n            new_index += (shape[0] * shape[1])\n            views.append(all_weights[index:new_index].reshape(shape[0], shape[1]))\n            index = new_index\n            \n            \n             \n        return all_weights, views\n                      \n                      \n    def __repr__(self):\n        return f\'NeuralNetwork({self.n_inputs}, \' + \\\n            f\'{self.n_hidden_units_by_layers}, {self.n_outputs})\'\n\n    def __str__(self):\n        s = self.__repr__()\n        if self.total_epochs > 0:\n            s += f\'\\n Trained for {self.total_epochs} epochs.\'\n            s += f\'\\n Final standardized training error {self.error_trace[-1]:.4g}.\'\n        return s\n \n    def train(self, X, T, n_epochs, method=\'sgd\', learning_rate=None, verbose=True):\n        """Updates the weights \n\n        Parameters\n        ----------\n        X : two-dimensional numpy array\n            number of samples  x  number of input components\n        T : two-dimensional numpy array\n            number of samples  x  number of output components\n        n_epochs : int\n            Number of passes to take through all samples\n        method : str\n            \'sgd\', \'adam\', or \'scg\'\n        learning_rate : float\n            Controls the step size of each update, only for sgd and adam\n        verbose: boolean\n            If True, progress is shown with print statements\n        """\n\n        # Calculate and assign standardization parameters\n        # ...\n\n\n            \n        self.X_means = X.mean(axis=0)\n        self.X_stds = X.std(axis=0)\n        self.T_means = T.mean(axis=0)\n        self.T_stds = T.std(axis=0)\n        \n        # Standardize X and T\n        # ...\n        XS = (X - self.X_means) / self.X_stds\n        TS = (T - self.T_means) / self.T_stds\n        \n        # Instantiate Optimizers object by giving it vector of all weights\n        optimizer = opt.Optimizers(self.all_weights)\n        error_convert_f = lambda err: (np.sqrt(err) * self.T_stds)[0]\n        # Call the requested optimizer method to train the weights.\n\n        if method == \'sgd\':\n            \n            error_trace = optimizer.sgd(self.error_f, self.gradient_f, [XS, TS], n_epochs, learning_rate, verbose,\n               error_convert_f=error_convert_f)\n\n        elif method == \'adam\':\n\n            error_trace = optimizer.adam(self.error_f, self.gradient_f, [XS, TS], n_epochs, learning_rate, verbose,\n               error_convert_f=error_convert_f)\n\n        elif method == \'scg\':\n\n            error_trace = optimizer.scg(self.error_f, self.gradient_f, [XS, TS], n_epochs, error_convert_f, verbose)\n\n        else:\n            raise Exception("method must be \'sgd\', \'adam\', or \'scg\'")\n\n        self.total_epochs += len(error_trace)\n        self.error_trace += error_trace\n\n        # Return neural network object to allow applying other methods\n        # after training, such as:    Y = nnet.train(X, T, 100, 0.01).use(X)\n\n        return self\n\n    def _forward(self, X):\n        """Calculate outputs of each layer given inputs in X\n        \n        Parameters\n        ----------\n        X : input samples, standardized\n\n        Returns\n        -------\n        Outputs of all layers as list\n        """\n        self.Ys = [X]\n        \n        # Append output of each layer to list in self.Ys, then return it.\n        # ...\n        #Also, need to add back in the sum for self.Ws[i][0:1, :])\n        if self.n_hidden_units_by_layers:\n            Z = np.tanh((X @ self.Ws[0][1:, :]) + self.Ws[0][0:1, :])\n            self.Ys.append(Z)\n            for i in range(len(self.Ws)-2):\n                Z = np.tanh((self.Ys[i + 1] @ self.Ws[i + 1][1:, :]) + self.Ws[i + 1][0:1, :])\n                self.Ys.append(Z)\n        # Output layer\n        Z = (self.Ys[-1] @ self.Ws[-1][1:, :]) + self.Ws[-1][0:1, :]\n        self.Ys.append(Z)\n        return self.Ys\n    \n    # Function to be minimized by optimizer method, mean squared error\n    def error_f(self, X, T):\n        """Calculate output of net and its mean squared error \n\n        Parameters\n        ----------\n        X : two-dimensional numpy array\n            number of samples  x  number of input components\n        T : two-dimensional numpy array\n            number of samples  x  number of output components\n\n        Returns\n        -------\n        Mean square error as scalar float that is the mean\n        square error over all samples\n        """\n        # Call _forward, calculate mean square error and return it.\n        # ...\n        return np.sqrt(np.mean((T - self._forward(X)[-1]) ** 2))\n\n#     Gradient of function to be minimized for use by optimizer method\n    def gradient_f(self, X, T):\n        """Returns gradient wrt all weights. Assumes _forward already called.\n\n        Parameters\n        ----------\n        X : two-dimensional numpy array\n            number of samples  x  number of input components\n        T : two-dimensional numpy array\n            number of samples  x  number of output components\n\n        Returns\n        -------\n        Vector of gradients of mean square error wrt all weights\n        """\n\n        # Assumes forward_pass just called with layer outputs saved in self.Ys.\n        n_samples = X.shape[0]\n        n_outputs = T.shape[1]\n        n_layers = len(self.n_hidden_units_by_layers) + 1\n\n        # D is delta matrix to be back propagated, only need division and negative on first step\n        D = -(T - self.Ys[-1]) / (n_samples * n_outputs)\n        # Step backwards through the layers to back-propagate the error (D)\n        for layeri in range(n_layers - 1, -1, -1):\n            \n            # gradient of all but bias weights\n            self.Grads[layeri][1:, :] = self.Ys[layeri].T @ D\n            # gradient of just the bias weights\n            self.Grads[layeri][0:1, :] = np.sum(D, axis=0)\n            # Back-propagate this layer\'s delta to previous layer\n            if layeri > 0:\n                D = D @ self.Ws[layeri][1:, :].T * (1-self.Ys[layeri]**2)\n                    \n        return self.all_gradients\n\n    def use(self, X):\n        """Return the output of the network for input samples as rows in X\n\n        Parameters\n        ----------\n        X : two-dimensional numpy array\n            number of samples  x  number of input components, unstandardized\n\n        Returns\n        -------\n        Output of neural network, unstandardized, as numpy array\n        of shape  number of samples  x  number of outputs\n        """\n\n        # Standardize X\n        # ...\n        XS = (X - self.X_means) / self.X_stds\n        \n        # Unstandardize output Y before returning it\n        \n        return self._forward(XS)[-1] * self.T_stds + self.T_means\n\n    def get_error_trace(self):\n        """Returns list of standardized mean square error for each epoch"""\n        return self.error_trace')


# ## Example Results

# Here we test the `NeuralNetwork` class with some simple data.  

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import neuralnetwork as nn

X = np.arange(-2, 2, 0.05).reshape(-1, 1)
T = np.sin(X) * np.sin(X * 10)

errors = []
n_epochs = 1000
method_rhos = [('sgd', 0.01),
               ('adam', 0.005),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(X.shape[1], [10, 10], 1)
    nnet.train(X, T, 50000, method=method, learning_rate=rho)
    Y = nnet.use(X)
    plt.plot(X, Y, 'o-', label='Model ' + method)
    errors.append(nnet.get_error_trace())

plt.plot(X, T, 'o', label='Train')
plt.xlabel('X')
plt.ylabel('T or Y')
plt.legend();


# In[3]:


plt.figure(2)
plt.clf()
for error_trace in errors:
    plt.plot(error_trace)
plt.xlabel('Epoch')
plt.ylabel('Standardized error')
plt.legend([mr[0] for mr in method_rhos]);


# In[4]:


import numpy as np
from neuralnetwork import NeuralNetwork
nn = NeuralNetwork(2, [2], 1)
X = np.array([[1,2],
    [4,5],
    [7,8]])
T=np.array([[4],
    [5],
    [6]])
nn.train(X, T, 3,  method='sgd', learning_rate=0.005, verbose=True)
print(nn.use(X))
print(str(nn))
# nn = NeuralNetwork(3, [3], 1)
# X = np.array([[1,2, 3],
#     [4,5,6],
#     [7,8,9]])
# T=np.array([[4],
#     [5],
#     [6]])
# nn.train(X, T, 3,  method='sgd', learning_rate=0.005, verbose=True)


# ## Application to Boston Housing Data

# Download data from [Boston House Data at Kaggle](https://www.kaggle.com/fedesoriano/the-boston-houseprice-data). Read it into python using the `pandas.read_csv` function.  Assign the first 13 columns as inputs to `X` and the final column as target values to `T`.  Make sure `T` is two-dimensional.

# Before training your neural networks, partition the data into training and testing partitions, as shown here.

# In[5]:


def partition(X, T, train_fraction):
    n_samples = X.shape[0]
    rows = np.arange(n_samples)
    np.random.shuffle(rows)
    
    n_train = round(n_samples * train_fraction)
    
    Xtrain = X[rows[:n_train], :]
    Ttrain = T[rows[:n_train], :]
    Xtest = X[rows[n_train:], :]
    Ttest = T[rows[n_train:], :]
    return Xtrain, Ttrain, Xtest, Ttest
def rmse(T, Y):
    return np.sqrt(np.mean((T - Y)**2))


# Write and run code using your NeuralNetwork class to model the Boston housing data. Experiment with all three optimization methods and a variety of neural network structures (numbers of hidden layer and units), learning rates, and numbers of epochs. Show results for at least three different network structures, learning rates, and numbers of epochs for each method. Show your results using print statements that include the method, network structure, number of epochs, learning rate, and RMSE on training data and RMSE on testing data.
# 
# Try to find good values for the RMSE on testing data. Discuss your results, including how good you think the RMSE values are by considering the range of house values given in the data. 

# In[6]:


import numpy as np
import pandas
import neuralnetwork as nn

data = pandas.read_csv('boston.csv')
data


# In[7]:


T = data.to_numpy()[:, -1].reshape(-1,1)
X = data.to_numpy()[:, 0:13]

print('T.max: ', data["MEDV"].max())
print('T.min: ', data["MEDV"].min())
# Assuming you have assigned `X` and `T` correctly.

Xtrain, Ttrain, Xtest, Ttest = partition(X, T, 0.8)  
Xtrain.shape, Ttrain.shape, Xtest.shape, Ttest.shape


# In[8]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 50000
method_rhos = [('sgd', 0.01),
               ('adam', 0.01),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [10, 10], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE on testing data = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 100000
method_rhos = [('sgd', 0.005),
               ('adam', 0.005),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [20, 20, 20], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE on testing data = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 75000
method_rhos = [('sgd', 0.05),
               ('adam', 0.05),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [5], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE test = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 10000
method_rhos = [('sgd', 0.05),
               ('adam', 0.05),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE test = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# Discussion: I started by taking a look at the data. I observed that the Median value of owner-occupied homes in \\$1000's or MEDV had a max of 50.0 and a min of 5.0. I thought this was a little low until I did some reading and realized the data was several decades old. I split the data into test and train. I used an 80/20 split test/train. I then used a for loop to test each method (sgd, adam, scg) using the same structure, learning rate, and number of epochs in each loop. I varied these 3 values across 4 total loops, testing 4 seperate scenarios for each method for a total of 12 different scenarios tested. In each loop I calculated the RMSE for train and test. 
# 
# I started using 50,000 epochs, a learning rate of 0.01 and 2 hidden layers with 10 units each. This was more or less an arbitrary choice. 
# 
# Seeing my results from above, I decided to try more complexity. For the next run I used 100,000 epochs, a learning rate of 0.005 and 3 hidden layers with 20 units each.
# 
# Seeing my results from above, I tried something a little more simple. For the next run I used 75,000 epochs, a learning rate of 0.05 and 1 hidden layer with 5 units each. n_epochs = 75000
# 
# 
# Finally I decided to try an incredibly simple approach. I used 10,000 epochs, a learning rate of 0.05 and no hidden layers. I essentially just did linear regression.

# # Grading
# 
# Your notebook will be run and graded automatically. Test this grading process by first downloading [A2grader.tar](http://www.cs.colostate.edu/~anderson/cs545/notebooks/A2grader.tar) and extract `A2grader.py` from it. Run the code in the following cell to demonstrate an example grading session.  The remaining 20 points will be based on your discussion of this assignment.
# 
# A different, but similar, grading script will be used to grade your checked-in notebook. It will include additional tests. You should design and perform additional tests on all of your functions to be sure they run correctly before checking in your notebook.  
# 
# For the grading script to run correctly, you must first name this notebook as 'Lastname-A2.ipynb' with 'Lastname' being your last name, and then save this notebook.

# In[ ]:


get_ipython().run_line_magic('run', '-i A2grader.py')


# # Extra Credit
# 
# Apply your multilayer neural network code to a regression problem using data that you choose 
# from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets.php). Pick a dataset that
# is listed as being appropriate for regression.

# In[ ]:


import pandas
data = pandas.read_csv('winequality-white.csv', delimiter=';', usecols=range(12))
data = data.dropna(axis=0)
data.shape
T = data.to_numpy()[:, -1].reshape(-1,1)
X = data.to_numpy()[:, 0:13]
print(X.shape)
print(T.shape)
Xtrain, Ttrain, Xtest, Ttest = partition(X, T, 0.8)  
Xtrain.shape, Ttrain.shape, Xtest.shape, Ttest.shape
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 75000
method_rhos = [('sgd', 0.01),
               ('adam', 0.01),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [10, 10, 10], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE test = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# In[ ]:


Xtrain, Ttrain, Xtest, Ttest = partition(X, T, 0.8)  
Xtrain.shape, Ttrain.shape, Xtest.shape, Ttest.shape
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
errors = []
n_epochs = 50000
method_rhos = [('sgd', 0.01),
               ('adam', 0.01),
               ('scg', None)]

for method, rho in method_rhos:
    nnet = nn.NeuralNetwork(Xtrain.shape[1], [], 1)
    nnet.train(Xtrain, Ttrain, n_epochs, method=method, learning_rate=rho, verbose=False)
    Ytrain = nnet.use(Xtrain)
    Ytest = nnet.use(Xtest)
    rmse_train = rmse(Ttrain, Ytrain)
    rmse_test = rmse(Ttest, Ytest)
    print( 'method = ', method, '\nnetwork structure = ', str(nnet), '\nnumber of epochs = ', n_epochs, '\nlearning rate = ', rho,
          '\nRMSE train = ', rmse_train, '\nRMSE test = ', rmse_test, '\n')
    errors.append(nnet.get_error_trace())


# In[ ]:





# In[ ]:




