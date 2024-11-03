import numpy as np
from collections import deque
import time

class MarketTrader:
    def __init__(self):
        self.price_history = {}  # Item price history
        self.inventory = {}      # Current inventory
        self.coins = 1000       # Starting coins
        self.price_window = 24   # Hours to analyze
        self.min_profit_margin = 0.15  # 15% minimum profit
        
    def update_price_history(self, item_id, current_price, timestamp):
        """Track price history for items"""
        if item_id not in self.price_history:
            self.price_history[item_id] = deque(maxlen=self.price_window)
        
        self.price_history[item_id].append({
            'price': current_price,
            'timestamp': timestamp
        })
    
    def analyze_market_trend(self, item_id):
        """Analyze price trends for an item"""
        if item_id not in self.price_history:
            return None
            
        prices = [entry['price'] for entry in self.price_history[item_id]]
        if len(prices) < 2:
            return None
            
        # Calculate key metrics
        mean_price = np.mean(prices)
        std_price = np.std(prices)
        current_price = prices[-1]
        price_change = (current_price - prices[0]) / prices[0]
        
        return {
            'mean_price': mean_price,
            'std_price': std_price,
            'current_price': current_price,
            'price_change': price_change,
            'volatility': std_price / mean_price
        }
    
    def should_buy(self, item_id, current_price):
        """Determine if item should be bought"""
        analysis = self.analyze_market_trend(item_id)
        if not analysis:
            return False
            
        # Buy conditions
        price_below_mean = current_price < analysis['mean_price']
        low_volatility = analysis['volatility'] < 0.2
        potential_profit = (analysis['mean_price'] - current_price) / current_price
        
        return (price_below_mean and 
                low_volatility and 
                potential_profit > self.min_profit_margin and
                self.coins >= current_price)
    
    def should_sell(self, item_id, current_price):
        """Determine if item should be sold"""
        if item_id not in self.inventory:
            return False
            
        analysis = self.analyze_market_trend(item_id)
        if not analysis:
            return False
            
        buy_price = self.inventory[item_id]['buy_price']
        profit_margin = (current_price - buy_price) / buy_price
        price_above_mean = current_price > analysis['mean_price']
        
        return profit_margin > self.min_profit_margin or price_above_mean
    
    def execute_trade(self, item_id, action, price, quantity=1):
        """Execute a buy or sell trade"""
        if action == 'buy':
            total_cost = price * quantity
            if self.coins >= total_cost:
                self.coins -= total_cost
                if item_id not in self.inventory:
                    self.inventory[item_id] = {
                        'quantity': 0,
                        'buy_price': 0
                    }
                # Update average buy price
                current_value = self.inventory[item_id]['buy_price'] * self.inventory[item_id]['quantity']
                new_value = price * quantity
                new_quantity = self.inventory[item_id]['quantity'] + quantity
                self.inventory[item_id]['buy_price'] = (current_value + new_value) / new_quantity
                self.inventory[item_id]['quantity'] += quantity
                return True
                
        elif action == 'sell':
            if item_id in self.inventory and self.inventory[item_id]['quantity'] >= quantity:
                self.coins += price * quantity
                self.inventory[item_id]['quantity'] -= quantity
                if self.inventory[item_id]['quantity'] == 0:
                    del self.inventory[item_id]
                return True
                
        return False
    
    def get_trade_recommendation(self, item_id, current_price):
        """Get trading recommendation for an item"""
        if self.should_buy(item_id, current_price):
            return {
                'action': 'buy',
                'confidence': self._calculate_buy_confidence(item_id, current_price)
            }
        elif self.should_sell(item_id, current_price):
            return {
                'action': 'sell',
                'confidence': self._calculate_sell_confidence(item_id, current_price)
            }
        return {
            'action': 'hold',
            'confidence': 1.0
        }
    
    def _calculate_buy_confidence(self, item_id, current_price):
        """Calculate confidence level for buying"""
        analysis = self.analyze_market_trend(item_id)
        if not analysis:
            return 0.0
            
        price_ratio = analysis['mean_price'] / current_price
        volatility_factor = 1 - analysis['volatility']
        trend_factor = 1 + analysis['price_change']
        
        confidence = (price_ratio * volatility_factor * trend_factor) / 3
        return min(max(confidence, 0.0), 1.0)
    
    def _calculate_sell_confidence(self, item_id, current_price):
        """Calculate confidence level for selling"""
        if item_id not in self.inventory:
            return 0.0
            
        analysis = self.analyze_market_trend(item_id)
        if not analysis:
            return 0.0
            
        buy_price = self.inventory[item_id]['buy_price']
        profit_ratio = (current_price - buy_price) / buy_price
        price_ratio = current_price / analysis['mean_price']
        volatility_factor = 1 - analysis['volatility']
        
        confidence = (profit_ratio * price_ratio * volatility_factor) / 3
        return min(max(confidence, 0.0), 1.0)