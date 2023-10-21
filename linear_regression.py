
def correlation(x,y):
	mean_x = sum(x)/len(x)
	mean_y = sum(y)/len(y)

	relationship = 0
	denominator_x = 0
	denominator_y = 0

	for i in range(len(sizes)):
	    relationship += (sizes[i] - mean_x) * (prices[i] - mean_y)
	    denominator_x += (sizes[i] - mean_x) ** 2
	    denominator_y += (prices[i] - mean_y) ** 2

	# Calculate the correlation coefficient (r)
	r = relationship/ (denominator_x * denominator_y) ** 0.5

	return r

def slope(x,y):
	mean_x = sum(x)/len(x)
	mean_y = sum(y)/len(y)

	# Calculate the values needed for slope (m) and y-intercept (b)
	numerator = 0
	denominator = 0

	for i in range(len(sizes)):
	    numerator += (sizes[i] - mean_x) * (prices[i] - mean_y)
	    denominator += (sizes[i] - mean_x) ** 2

	m = numerator / denominator

	return m


def intercept(x,y):
	mean_x = sum(x)/len(x)
	mean_y = sum(y)/len(y)

	# Calculate the values needed for slope (m) and y-intercept (b)
	numerator = 0
	denominator = 0

	for i in range(len(sizes)):
	    numerator += (sizes[i] - mean_x) * (prices[i] - mean_y)
	    denominator += (sizes[i] - mean_x) ** 2

	m = numerator / denominator
	b = mean_y - m * mean_x

	return b


def predict_value(x,y, value):
	mean_x = sum(x)/len(x)
	mean_y = sum(y)/len(y)

	# Calculate the values needed for slope (m) and y-intercept (b)
	numerator = 0
	denominator = 0

	for i in range(len(sizes)):
	    numerator += (sizes[i] - mean_x) * (prices[i] - mean_y)
	    denominator += (sizes[i] - mean_x) ** 2

	m = numerator / denominator
	b = mean_y - m * mean_x

	predicted_value = m * value + b

	return predicted_value


