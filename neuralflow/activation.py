from __future__ import annotations

from enum import Enum
import math
import numpy as np

class ActivationFunction(Enum):
    linear = 0
    relu = 1
    leakyrelu = 2
    tanh = 3
    sigmoid = 4
    
    def getFunction(activation : ActivationFunction):
        if activation == ActivationFunction.linear:
            return np.vectorize(ActivationFunction.linearFunc)
        elif activation == ActivationFunction.relu:
            return np.vectorize(ActivationFunction.reluFunc)
        elif activation == ActivationFunction.leakyrelu:
            return  np.vectorize(ActivationFunction.leakyReluFunc)
        elif activation == ActivationFunction.tanh:
            return np.vectorize(ActivationFunction.tanhFunc)
        elif activation == ActivationFunction.sigmoid:
            return np.vectorize(ActivationFunction.sigmoidFunc)
        else:
            raise ValueError("Invalid Activation Function")
    
    def getGradient(activation : ActivationFunction):
        if activation == ActivationFunction.linear:
            return np.vectorize(ActivationFunction.linearGradient)
        elif activation == ActivationFunction.relu:
            return np.vectorize(ActivationFunction.reluGradient)
        elif activation == ActivationFunction.leakyrelu:
            return  np.vectorize(ActivationFunction.leakyReluGradient)
        elif activation == ActivationFunction.tanh:
            return np.vectorize(ActivationFunction.tanhGradient)
        elif activation == ActivationFunction.sigmoid:
            return np.vectorize(ActivationFunction.sigmoidGradient)
        else:
            raise ValueError("Invalid Activation Function")

    def linearFunc(x):
        return x
    def linearGradient(x):
        return 1
    
    def reluFunc(x):
        return max(0.0,x)
    def reluGradient(x):
        if x>0:
            return 1
        elif x<0:
            return 0
        else:
            return 1e-7

    def leakyReluFunc(x):
        return max(0,x) + 1e-2*min(0,x)
    def leakyReluGradient(x):
        if x>0:
            return 1
        elif x<0:
            return 1e-2
        else:
            return 1e-7

    def tanhFunc(x):
        return math.tanh(x)
    def tanhGradient(x):
        return 1 - math.tanh(x)**2
    
    def sigmoidFunc(x):
        return 1/(1+ math.exp(-x))
    def sigmoidGradient(x):
        return ActivationFunction.sigmoidFunc(x)*(1-ActivationFunction.sigmoidFunc(x))


    