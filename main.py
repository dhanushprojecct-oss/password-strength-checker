import re
import sys
from getpass import getpass

# Load common passwords from file
def load_common_passwords():
    try:
        with open("common_passwords.txt", "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return ["password", "123456", "qwerty", "admin"]


def has_sequential_pattern(password):
    sequences = ["123", "abc", "qwerty"]
    for seq in sequences:
        if seq in password.lower():
            return True
    return False


def has_repeated_chars(password):
    return re.search(r"(.)\1\1", password) is not None


def check_password_strength(password, common_passwords):
    score = 0
    feedback = []

    # Length
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password must be at least 8 characters")

    if len(password) >= 12:
        score += 1

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    # Digits
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers")

    # Special characters
    if re.search(r"[^a-zA-Z0-9\s]", password):
        score += 2
    else:
        feedback.append("Add special characters")

    # Common password check
    if password.lower() in common_passwords:
        feedback.append("Avoid common passwords")
    else:
        score += 2

    # Pattern checks
    if has_sequential_pattern(password):
        feedback.append("Avoid sequential patterns like 123 or abc")
        score -= 1

    if has_repeated_chars(password):
        feedback.append("Avoid repeated characters like aaa")
        score -= 1

    # Cap score for critical flaws
    if len(password) < 8 or password.lower() in common_passwords:
        score = min(score, 3)

    # Ensure score remains within bounds
    score = max(0, min(score, 10))

    return score, feedback


def get_strength(score):
    if score <= 3:
        return "Weak"
    elif score <= 6:
        return "Medium"
    else:
        return "Strong"


def show_strength_meter(score):
    print("Strength Meter:", "#" * score + "-" * (10 - score))


# MAIN PROGRAM
common_passwords = load_common_passwords()

# CLI support
if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    password = getpass("Enter password: ")

score, feedback = check_password_strength(password, common_passwords)

print("\nPassword Analysis")
print("-----------------")
print("Score:", score, "/10")
print("Strength:", get_strength(score))

show_strength_meter(score)

if feedback:
    print("\nSuggestions:")
    for f in feedback:
        print("-", f)
else:
    print("Excellent password.")