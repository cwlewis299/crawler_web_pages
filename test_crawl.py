import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_query_params(self):
        input_url = "https://www.boot.dev/blog/path?query=param"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_fragment(self):
        input_url = "https://www.boot.dev/blog/path#section"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_port(self):
        input_url = "https://www.boot.dev:8080/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_dot_com(self):
        input_url = "https://www.youtube.com"
        actual = normalize_url(input_url)
        expected = "www.youtube.com"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_subdomain(self):
        input_url = "https://subdomain.example.com/path"
        actual = normalize_url(input_url)
        expected = "subdomain.example.com/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_IPv4_address(self):
        input_url = "https://192.168.1.1/path"
        actual = normalize_url(input_url)
        expected = "192.168.1.1/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_empty_path(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_IPv6_address(self):
        input_url = "https://[2001:db8::1]/path"
        actual = normalize_url(input_url)
        expected = "[2001:db8::1]/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_long_IPv6_address(self):
        input_url = "https://[2001:db8:ffff:ffff:ffff:ffff:ffff:ffff]/path"
        actual = normalize_url(input_url)
        expected = "[2001:db8:ffff:ffff:ffff:ffff:ffff:ffff]/path"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()