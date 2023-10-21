import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def predict(weights, features, bias):
    z = sum([weights[i] * features[i] for i in range(len(weights))]) + bias
    return sigmoid(z)

def update_weights(features, label, weights, bias, learning_rate):
    prediction = predict(weights, features, bias)
    gradient = prediction - label
    
    # Update weights
    for i in range(len(weights)):
        weights[i] -= learning_rate * gradient * features[i]
    
    # Update bias
    bias -= learning_rate * gradient
    
    return weights, bias

def train(features_set, labels, weights, bias, learning_rate, epochs):
    for epoch in range(epochs):
        for features, label in zip(features_set, labels):
            weights, bias = update_weights(features, label, weights, bias, learning_rate)
    return weights, bias




