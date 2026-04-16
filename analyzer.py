import re
import math

def load_file(filename, fallback):
    try:
        with open(filename, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return fallback

# Load common passwords at module level
COMMON_PASSWORDS = load_file("common_passwords.txt", ["password", "123456", "qwerty", "admin"])

def has_sequential_pattern(password):
    sequences = ["123", "abc", "qwerty"]
    lowered = password.lower()
    for seq in sequences:
        if seq in lowered:
            return True
    return False

def has_repeated_chars(password):
    return re.search(r"(.)\1\1", password) is not None

def calculate_entropy(password):
    # Determine the character set size based on characters used
    pool_size = 0
    if re.search(r"[a-z]", password): pool_size += 26
    if re.search(r"[A-Z]", password): pool_size += 26
    if re.search(r"[0-9]", password): pool_size += 10
    if re.search(r"[^a-zA-Z0-9\s]", password): pool_size += 32
    if " " in password: pool_size += 1
    
    if pool_size == 0 or len(password) == 0:
        return 0
    return len(password) * math.log2(pool_size)

def analyze_password(password):
    score = 0
    feedback = []

    # Length
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password must be at least 8 characters.")

    if len(password) >= 12:
        score += 1

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Digits
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # Special characters
    if re.search(r"[^a-zA-Z0-9\s]", password):
        score += 2
    else:
        feedback.append("Add special characters.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Avoid common passwords.")
    else:
        score += 2

    # Pattern checks
    if has_sequential_pattern(password):
        feedback.append("Avoid sequential patterns like 123 or abc.")
        score -= 1

    if has_repeated_chars(password):
        feedback.append("Avoid repeated characters like aaa.")
        score -= 1

    # Cap score for critical flaws
    if len(password) < 8 or password.lower() in COMMON_PASSWORDS:
        score = min(score, 3)

    # Ensure score remains within bounds
    score = max(0, min(score, 10))
    
    # Calculate entropy
    entropy = round(calculate_entropy(password), 2)
    
    # Determine strength
    if score <= 4:
        strength = "Weak"
    elif score <= 7:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "score": score,
        "strength": strength,
        "entropy": entropy,
        "feedback": feedback
    }
