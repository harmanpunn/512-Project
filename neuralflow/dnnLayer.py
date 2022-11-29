from activation import ActivationFunction
import numpy as np

class DNNLayer:
    def __init__(self, input, output, batchSize  = 1, weights = None, bias = None, activation = ActivationFunction.relu) -> None:
        self.activationFunction = ActivationFunction.getFunction(activation)
        self.activationGradient = ActivationFunction.getGradient(activation)
        
        self.input = input
        self.output = output
        self.batchSize = batchSize

        self.weights = np.random.rand(self.output, self.input) if weights == None else weights
        self.bias = np.random.rand(self.output, self.batchSize) if bias == None else bias

    def forward(self, x):
        x = np.array(x)
        if x.transpose().shape!=(self.input,self.batchSize):
            raise ValueError("Expected input of size",(self.input,self.batchSize)," got ",x.transpose().shape," instead")
        
        return self.activationFunction(np.add(np.matmul(self.weights, x.transpose()),self.bias)).transpose()
        
# layer = DNNLayer(2,3)

# print(layer.forward([[1,2]]))