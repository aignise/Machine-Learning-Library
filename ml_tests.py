import linear_regression
import logistic_regression 

def logistic_test():

	# Hours studied = [2, 3, 5, 7, 10]
	# Pass (1) or Fail (0) = [0, 0, 1, 1, 1]

	features_set = [[2], [3], [5], [7], [10]]
	labels = [0, 0, 1, 1, 1]

	# Initialize weights and bias
	weights = [0]
	bias = 0

	# Train the model
	weights, bias = train(features_set, labels, weights, bias, learning_rate=0.01, epochs=1000)

	# Predict for a new student who studied for 6 hours
	prediction = predict(weights, [6], bias)
	print("Probability of passing:", prediction)