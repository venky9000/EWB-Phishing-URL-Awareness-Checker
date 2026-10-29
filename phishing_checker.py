"""EWB Phishing URL Awareness Checker.

This educational program inspects URL text only. It never opens URLs or
makes network requests.
"""

import re
from urllib.parse import urlparse


def inspect_url(raw_url):
    """Return plain-language findings for selected URL warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    # Match the workbook's beginner-friendly behaviour when a scheme is missing.
    candidate = url if "://" in url else "http://" + url

    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["This text is not a valid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    # Check 1: user information before @ can make a hostname misleading.
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Check 2: more than 100 characters.
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Check 3: a hostname shaped like four dot-separated number groups.
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Check 4: five or more hostname labels separated by dots.
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Check 5: punycode-style marker in the hostname.
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # Check 6: plain HTTP scheme.
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def main():
    """Run an interactive command-line session."""
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")

    while True:
        try:
            raw_url = input("\nEnter a sample URL to inspect (or type q to quit): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Stay alert online.")
            break

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)
        print("\nResult:")
        for item in findings:
            print("- " + item)

        # Information messages are not counted as warning signs.
        if findings and not findings[0].startswith(
            ("No URL entered.", "Could not identify", "This text is not a valid URL",
             "No listed warning signs")
        ):
            print(f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found.")

        print("Never enter passwords from unexpected links.")
        print("This educational checker is not a complete phishing detector.")


if __name__ == "__main__":
    main()
