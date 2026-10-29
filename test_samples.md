# Test Results — EWB Phishing URL Awareness Checker

- **Test date:** 2026-10-29
- **Operating system:** Linux-6.18.55-x86_64-with-glibc2.41 (the generation/test environment; not the user's Windows computer)
- **Python version actually used:** Python 3.13.5
- **Automated test command:** `python -m unittest discover -s tests -v`
- **Automated test run exit code:** 0

## Five workbook sample URLs

| # | Exact URL | Expected result | Actual result | Status |
|---|---|---|---|---|
| 1 | `https://www.example.com/login` | No listed warning signs found. This does NOT prove safety. | No listed warning signs found. This does NOT prove safety. | PASS |
| 2 | `http://192.0.2.10/account` | Uses an IP address instead of a familiar domain.; Uses HTTP. HTTPS alone does not prove trust. | Uses an IP address instead of a familiar domain.; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 3 | `http://example.com@sample.invalid/login` | Contains an @ symbol; inspect carefully.; Uses HTTP. HTTPS alone does not prove trust. | Contains an @ symbol; inspect carefully.; Uses HTTP. HTTPS alone does not prove trust. | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Contains many hostname segments/subdomains. | Contains many hostname segments/subdomains. | PASS |
| 5 | `https://xn--example.invalid/` | Contains a punycode-style hostname. | Contains a punycode-style hostname. | PASS |

## Notes and correction

The code uses Python's URL parser to read the actual hostname. For
`http://example.com@sample.invalid/login`, the hostname is `sample.invalid`;
the `example.com` text is user information before the `@` symbol. The parser
also catches malformed bracketed URL input such as `http://[bad` and returns
a message instead of allowing a `ValueError` to stop the program.

Statuses above are based on the observed command-line output in this
environment. Re-run the commands on your Windows computer before describing
them as results from your own computer.

## Reflection

“While testing the URLs, I learned that the `@` symbol can make a link misleading because the actual hostname may be different from what I first notice. I also understood that a URL with no warning signs is not automatically safe, because this program checks only a few patterns.”
