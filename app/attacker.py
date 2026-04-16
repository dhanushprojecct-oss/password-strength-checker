import time

def load_wordlist(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return ["password", "123456", "qwerty"]

class Attacker:
    def __init__(self, wordlist_file="data/wordlist.txt"):
        self.wordlist = load_wordlist(wordlist_file)

    def simulate_dictionary_attack(self, password):
        start_time = time.time()
        
        success = False
        target = password.lower()
        for word in self.wordlist:
            if word == target:
                success = True
                break
                
        elapsed_time = time.time() - start_time
        
        return {
            "success": success,
            "time_taken_ms": round(elapsed_time * 1000, 4)
        }
        
    def format_time(self, seconds):
        if seconds < 1:
            return "Instantly"
        elif seconds < 60:
            return f"{round(seconds)} seconds"
        elif seconds < 3600:
            return f"{round(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{round(seconds/3600)} hours"
        elif seconds < 31536000:
            return f"{round(seconds/86400)} days"
        else:
            years = seconds / 31536000
            if years > 1e12:
                return "Trillions of years"
            elif years > 1e9:
                return f"{round(years/1e9, 1)} billion years"
            elif years > 1e6:
                return f"{round(years/1e6, 1)} million years"
            return f"{round(years)} years"

    def estimate_brute_force(self, password):
        from app.analyzer import calculate_entropy
        import math
        
        # Determine pool size
        pool_size = 0
        from string import ascii_lowercase, ascii_uppercase, digits
        if any(c in ascii_lowercase for c in password): pool_size += 26
        if any(c in ascii_uppercase for c in password): pool_size += 26
        if any(c in digits for c in password): pool_size += 10
        if any(c not in ascii_lowercase+ascii_uppercase+digits for c in password): pool_size += 32
        
        if pool_size == 0 or len(password) == 0:
            return {"crack_time": "Instantly", "risk_level": "High"}
            
        # Combinations
        try:
            combinations = pool_size ** len(password)
        except OverflowError:
            return {"crack_time": "Trillions of years", "risk_level": "Low"}
            
        # Assume an attacker can test 100 billion passwords per second
        # (A modern high-end GPU cluster standard estimate)
        guesses_per_second = 100_000_000_000 
        seconds = combinations / guesses_per_second
        
        crack_time = self.format_time(seconds)
        
        if seconds < 86400: # Less than a day
            risk_level = "High"
        elif seconds < 31536000: # Less than a year
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        return {
            "crack_time": crack_time,
            "risk_level": risk_level,
            "seconds": seconds
        }
