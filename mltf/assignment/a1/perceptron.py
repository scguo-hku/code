# Task 1: import the necessary libraries
import numpy as np

class Perceptron:
    # Constructor
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        # Task 2: initialization
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    # Training
    def fit(self, X, y):
        # Task 3: train the perceptron
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.errors_ = []

        for i in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
            print(f'Epoch {i+1}/{self.n_iter}, Errors: {errors}')
        return self
    
    # Net input
    def net_input(self, X):
        # Task 4: calculates the net input
        return np.dot(X, self.w_[1:]) + self.w_[0]

    # Decision
    def predict(self, X):
        # Task 5: make the binary decision/prediction
        return np.where(self.net_input(X) >= 0.0, 1, -1)