import numpy as np
import random
from collections import deque

class CrossoutAI:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # Size of game state (positions, health, etc.)
        self.action_size = action_size  # Number of possible actions
        self.memory = deque(maxlen=2000)  # Experience replay memory
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Simple neural network using numpy
        self.weights1 = np.random.randn(self.state_size, 24)
        self.weights2 = np.random.randn(24, 24)
        self.weights3 = np.random.randn(24, self.action_size)
        return {'w1': self.weights1, 'w2': self.weights2, 'w3': self.weights3}

    def _relu(self, x):
        return np.maximum(0, x)

    def _forward(self, state):
        layer1 = self._relu(np.dot(state, self.model['w1']))
        layer2 = self._relu(np.dot(layer1, self.model['w2']))
        return np.dot(layer2, self.model['w3'])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self._forward(state))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self._forward(next_state))

            target_f = self._forward(state)
            target_f[action] = target

            # Simple gradient descent update
            self._update_weights(state, target_f)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def _update_weights(self, state, target):
        # Simplified backpropagation
        learning_rate = self.learning_rate
        delta = target - self._forward(state)
        
        # Update weights using gradient descent
        self.model['w3'] += learning_rate * delta.reshape(-1, 1)
        self.model['w2'] += learning_rate * delta.reshape(-1, 1)
        self.model['w1'] += learning_rate * delta.reshape(-1, 1)

# Example usage
def main():
    # Define state and action space sizes
    state_size = 10  # Example: position, speed, health, enemies positions, etc.
    action_size = 4  # Example: move forward, backward, shoot, strafe

    # Initialize AI
    ai = CrossoutAI(state_size, action_size)
    
    # Training loop (simplified example)
    episodes = 100
    batch_size = 32

    for episode in range(episodes):
        # Initialize game state (would come from Crossout game)
        state = np.random.random(state_size)
        
        for time_step in range(500):  # Max steps per episode
            # Get action from AI
            action = ai.act(state)
            
            # Execute action in game (simplified simulation)
            next_state = np.random.random(state_size)  # Would come from game
            reward = random.random()  # Would come from game performance
            done = random.random() > 0.95  # Episode end condition
            
            # Store experience
            ai.remember(state, action, reward, next_state, done)
            
            # Move to next state
            state = next_state
            
            # Train on past experiences
            if len(ai.memory) > batch_size:
                ai.replay(batch_size)
                
            if done:
                print(f"Episode: {episode+1}, Score: {time_step}")
                break

if __name__ == "__main__":
    main()