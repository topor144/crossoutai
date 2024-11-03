import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0/input_size)
        self.weights2 = np.random.randn(hidden_size, hidden_size) * np.sqrt(2.0/hidden_size)
        self.weights3 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0/hidden_size)
        
        # Weight constraints
        self.max_weight_value = 2.0
        self.min_weight_value = -2.0
        
        # Error tracking
        self.error_threshold = 0.5
        self.error_history = []
        self.max_error_history = 1000

    def forward(self, state):
        self.layer1 = self._relu(np.dot(state, self.weights1))
        self.layer2 = self._relu(np.dot(self.layer1, self.weights2))
        return np.dot(self.layer2, self.weights3)

    def _relu(self, x):
        return np.maximum(0, x)

    def _clip_weights(self):
        """Constrain weights within defined bounds"""
        self.weights1 = np.clip(self.weights1, self.min_weight_value, self.max_weight_value)
        self.weights2 = np.clip(self.weights2, self.min_weight_value, self.max_weight_value)
        self.weights3 = np.clip(self.weights3, self.min_weight_value, self.max_weight_value)

    def _track_error(self, error):
        """Track prediction errors for analysis"""
        self.error_history.append(error)
        if len(self.error_history) > self.max_error_history:
            self.error_history.pop(0)

    def is_prediction_reliable(self, prediction, actual):
        """Check if the prediction error is within acceptable bounds"""
        error = np.mean(np.abs(prediction - actual))
        self._track_error(error)
        return error < self.error_threshold

    def update(self, state, delta, learning_rate):
        # Backpropagation with error tracking
        self.weights3 += learning_rate * np.outer(self.layer2, delta)
        self.weights2 += learning_rate * np.outer(self.layer1, delta)
        self.weights1 += learning_rate * np.outer(state, delta)
        
        # Apply weight constraints
        self._clip_weights()
        
        # Track error
        self._track_error(np.mean(np.abs(delta)))