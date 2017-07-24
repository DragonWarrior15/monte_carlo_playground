import numpy as np

class multi_layer_perceptron():
    '''
    a simple mlp class to calculate an output based on a input vector
    pass the input layer size, sizes of the hidden layers, size of the output layer
    '''
    def __init__(self, input_layer_size, output_layer_size, hidden_layers = [], random_state = None):
        self.input_layer_size = input_layer_size
        self.hidden_layers = hidden_layers
        self.output_layer_size = output_layer_size

        np.random.seed(random_state)
        self.gaussian_mean = 0
        self.gaussian_var = 1

        # initialize the weights
        self.weights = []
        self.bias = []

        if len(self.hidden_layers) == 0:
            self.weights = [np.random.normal(self.gaussian_mean, self.gaussian_var, [input_layer_size, output_layer_size])]
            self.bias = np.random.normal(self.gaussian_mean, self.gaussian_var, [1, 1])
        else:
            for i in range(len(self.hidden_layers) + 1):
                if i == 0:
                    self.weights.append(np.random.normal(self.gaussian_mean, self.gaussian_var, (self.input_layer_size, self.hidden_layers[0])))
                elif i == len(hidden_layers):
                    self.weights.append(np.random.normal(self.gaussian_mean, self.gaussian_var, (self.hidden_layers[-1], output_layer_size)))
                else:
                    self.weights.append(np.random.normal(self.gaussian_mean, self.gaussian_var, (self.hidden_layers[i - 1], self.hidden_layers[i])))
            self.bias = np.random.normal(self.gaussian_mean, self.gaussian_var, [len(self.hidden_layers) + 1, 1])

    def predict(self, input_vector):
        f = lambda x: 1/(1 + np.exp(-x))
        input_vector = np.array(input_vector).reshape(-1, self.input_layer_size)
        output = f(np.matmul(input_vector, self.weights[0]) + self.bias[0])
        for i in range(1, len(self.weights)):
            output = f((np.matmul(output, self.weights[i]) + self.bias[i]))

        output = np.exp(output)/np.sum(np.exp(output))
        return (output)

    def get_weights(self):
        return (self.weights)

    def get_bias(self):
        return (self.bias)

    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias

    def tweak_weights(self):
        num_weights = len(self.weights)
        for i in range(num_weights):
            self.weights[i] += np.random.normal(self.gaussian_mean, self.gaussian_var, self.weights[i].shape)

    def tweak_bias(self):
        num_bias = len(self.bias)
        for i in range(num_bias):
            self.bias[i] += np.random.normal(self.gaussian_mean, self.gaussian_var, self.bias[i].shape)        


def main():
    # simple main function to check if the class is working fine
    print ('mlp1')
    mlp1 = multi_layer_perceptron(3, 1, [2])
    print (mlp1.get_weights())
    print ([x.shape for x in mlp1.get_weights()])
    print (mlp1.get_bias())
    print (mlp1.predict([1, 2, 3]))

    print ('mlp2')
    mlp2 = multi_layer_perceptron(3, 1)
    print (mlp2.get_weights())
    print ([x.shape for x in mlp2.get_weights()])
    print (mlp2.get_bias())
    print (mlp2.predict([1, 2, 3]))

if __name__ == "__main__":
    main()