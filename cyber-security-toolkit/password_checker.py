"""Password strength checker: scores a password and gives improvement tips."""
import math
import string
import sys
import getpass

COMMON = {"password", "123456", "12345678", "qwerty", "abc123", "admin",
          "letmein", "welcome", "iloveyou", "password1", "india123"}


def entropy_bits(password: str) -> float:
    """Estimate entropy = length * log2(character pool size)."""
    pool = 0
    if any(c in string.ascii_lowercase for c in password): pool += 26
    if any(c in string.ascii_uppercase for c in password): pool += 26
    if any(c in string.digits for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += len(string.punctuation)
    return len(password) * math.log2(pool) if pool else 0.0


def check(password: str):
    tips = []
    if password.lower() in COMMON:
        return "VERY WEAK", 0.0, ["This is a commonly used password."]
    if len(password) < 12: tips.append("Use at least 12 characters.")
    if not any(c.isupper() for c in password): tips.append("Add uppercase letters.")
    if not any(c.islower() for c in password): tips.append("Add lowercase letters.")
    if not any(c.isdigit() for c in password): tips.append("Add digits.")
    if not any(c in string.punctuation for c in password): tips.append("Add symbols.")
    if len(set(password)) < len(password) / 2: tips.append("Avoid many repeated characters.")

    bits = entropy_bits(password)
    if bits < 28: label = "VERY WEAK"
    elif bits < 36: label = "WEAK"
    elif bits < 60: label = "MODERATE"
    elif bits < 80: label = "STRONG"
    else: label = "VERY STRONG"
    return label, bits, tips


if __name__ == "__main__":
    pw = sys.argv[1] if len(sys.argv) > 1 else getpass.getpass("Enter password: ")
    label, bits, tips = check(pw)
    print(f"Strength: {label} (~{bits:.1f} bits of entropy)")
    for t in tips:
        print(" -", t)
