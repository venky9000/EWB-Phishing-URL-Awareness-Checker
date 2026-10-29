"""Deterministic tests for the EWB Phishing URL Awareness Checker."""

import unittest

from phishing_checker import inspect_url


class InspectURLTests(unittest.TestCase):
    def test_at_symbol_and_actual_hostname_parsing(self):
        findings = inspect_url("http://example.com@sample.invalid/login")
        self.assertIn("Contains an @ symbol; inspect carefully.", findings)
        self.assertIn("Uses HTTP. HTTPS alone does not prove trust.", findings)
        # The actual parsed hostname is sample.invalid, not example.com.
        self.assertNotIn(
            "Uses an IP address instead of a familiar domain.", findings
        )
        self.assertNotIn("Contains many hostname segments/subdomains.", findings)

    def test_long_url_over_100_characters(self):
        url = "https://example.invalid/" + ("a" * 90)
        self.assertGreater(len(url), 100)
        self.assertIn(
            "Unusually long URL (over 100 characters).", inspect_url(url)
        )

    def test_ipv4_looking_hostname(self):
        findings = inspect_url("http://192.0.2.10/account")
        self.assertIn(
            "Uses an IP address instead of a familiar domain.", findings
        )

    def test_five_or_more_hostname_labels(self):
        findings = inspect_url("https://a.b.c.d.e.example.invalid/path")
        self.assertIn(
            "Contains many hostname segments/subdomains.", findings
        )

    def test_punycode_marker(self):
        findings = inspect_url("https://xn--example.invalid/")
        self.assertIn("Contains a punycode-style hostname.", findings)

    def test_http_scheme(self):
        findings = inspect_url("http://example.invalid/")
        self.assertIn(
            "Uses HTTP. HTTPS alone does not prove trust.", findings
        )

    def test_no_warning_disclaimer(self):
        findings = inspect_url("https://www.example.com/login")
        self.assertEqual(
            findings,
            ["No listed warning signs found. This does NOT prove safety."]
        )

    def test_empty_input(self):
        self.assertEqual(inspect_url("  "), ["No URL entered."])

    def test_missing_hostname(self):
        self.assertEqual(
            inspect_url("http://"),
            ["Could not identify a hostname."]
        )

    def test_malformed_bracketed_url(self):
        self.assertEqual(
            inspect_url("http://[bad"),
            ["This text is not a valid URL format."]
        )

    def test_missing_scheme_is_treated_as_http(self):
        self.assertIn(
            "Uses HTTP. HTTPS alone does not prove trust.",
            inspect_url("www.example.com")
        )


if __name__ == "__main__":
    unittest.main()
