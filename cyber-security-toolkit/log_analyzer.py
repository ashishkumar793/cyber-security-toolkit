"""Detect possible brute-force attacks from an auth log.

Usage: python log_analyzer.py sample/auth.log [threshold]
Flags IP addresses with `threshold` or more failed logins (default 5).
"""
import re
import sys
from collections import Counter

FAILED = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)")


def analyze(path: str, threshold: int = 5):
    by_ip, by_user = Counter(), Counter()
    with open(path) as f:
        for line in f:
            m = FAILED.search(line)
            if m:
                by_user[m.group(1)] += 1
                by_ip[m.group(2)] += 1
    print(f"Total failed logins: {sum(by_ip.values())}")
    print("\nSuspicious IPs:")
    flagged = [(ip, n) for ip, n in by_ip.most_common() if n >= threshold]
    for ip, n in flagged:
        print(f"  {ip}: {n} failed attempts")
    if not flagged:
        print("  none")
    print("\nMost targeted usernames:")
    for u, n in by_user.most_common(3):
        print(f"  {u}: {n}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    analyze(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5)
