# Cyber Security Toolkit

Three small defensive security tools written in Python (no external libraries).

| Tool | Concept | Run |
|------|---------|-----|
| `password_checker.py` | Entropy and password policy | `python password_checker.py` |
| `file_integrity.py` | Hashing (SHA-256), tamper detection | `python file_integrity.py init sample` then `check sample` |
| `log_analyzer.py` | Brute-force detection from logs | `python log_analyzer.py sample/auth.log` |

## How it works
- **Password checker:** entropy = length x log2(character pool size), plus a common-password list.
- **File integrity:** stores a SHA-256 hash of every file; any change in content changes the hash.
- **Log analyzer:** regex finds "Failed password" lines and counts attempts per IP.

## Disclaimer
Educational project. The log file in `sample/` uses reserved documentation IPs and is fictional.
