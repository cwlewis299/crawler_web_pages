import unittest
from crawl import get_first_paragraph_from_html, normalize_url, get_heading_from_html, get_urls_from_html, get_images_from_html


class TestCrawl(unittest.TestCase):
    # Normalize URL Tests
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

    def test_normalize_url_with_IPv6_address_and_port(self):
        input_url = "https://[2001:db8::1]:8080/path"
        actual = normalize_url(input_url)
        expected = "[2001:db8::1]/path"
        self.assertEqual(actual, expected)

    # Get Heading from HTML Tests
    def test_html_heading_extraction_basic(self):
        html = "<html><body><h1>Test Heading</h1></body></html>"
        actual = get_heading_from_html(html)
        expected = "Test Heading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_no_heading(self):
        html = "<html><body><p>No heading here</p></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_multiple_headings(self):
        html = "<html><body><h1>First Heading</h1><h2>Second Heading</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "First Heading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_only_h2(self):
        html = "<html><body><h2>Only H2 Heading</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "Only H2 Heading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_headings_and_paragraphs(self):
        html = "<html><body><h1>Main Heading</h1><p>Some text</p><h2>Subheading</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "Main Heading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_h2_and_paragraph(self):
        html = "<html><body><h2>Subheading</h2><p>Some text</p></body></html>"
        actual = get_heading_from_html(html)
        expected = "Subheading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_paragraph_before_heading(self):
        html = "<html><body><p>Some text</p><h1>Main Heading</h1></body></html>"
        actual = get_heading_from_html(html)
        expected = "Main Heading"
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_paragraph_without_heading(self):
        html = "<html><body><p>Some text</p></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_paragraphs_and_no_headings(self):
        html = "<html><body><p>Paragraph 1</p><p>Paragraph 2</p></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_empty_html(self):
        html = ""
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_h3(self):
        html = "<html><body><h3>Heading 3</h3></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_html_heading_extraction_with_multiple_headings_that_are_not_h1_or_h2(self):
        html = "<html><body><h3>Heading 3</h3><h4>Heading 4</h4></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    # Get First Paragraph from HTML Tests
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph</p>
            <main>
                <p>Main paragraph</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>First paragraph</p>
            <p>Second paragraph</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraphs(self):
        input_body = """<html><body>
            <main></main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty_html(self):
        input_body = ""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_with_header_without_paragraph(self):
        input_body = """<html><body>
            <main>
                <h1>Main Heading</h1>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_with_multiple_paragraphs_inside_and_outside(self):
        input_body = """<html><body>
            <p>Outside paragraph</p>
            <main>
                <p>First main paragraph</p>
                <p>Second main paragraph</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First main paragraph"
        self.assertEqual(actual, expected)

    # Get URLS from HTML Tests
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_in_folder(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="about.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_in_subfolder(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="subfolder/about.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/subfolder/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_in_parent_folder(self):
        input_url = "https://crawler-test.com/subfolder/"
        input_body = '<html><body><a href="../about.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_in_folder_explicit(self):
        input_url = "https://crawler-test.com/"
        input_body = '<html><body><a href="./about.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_in_root_relative(self):
        input_url = "https://crawler-test.com/subfolder/sub1/sub2/"
        input_body = '<html><body><a href="/about.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>This is a paragraph.</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a>' \
        '<a href="about.html"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_with_image(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><img src="image.jpg" alt="Image"></a>' \
        '<a href="about.html"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about.html"]
        self.assertEqual(actual, expected)

    # Get Images from HTML Tests
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo">' \
        '<img src="https://crawler-test.com/banner.png" alt="Banner"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/banner.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>No images here</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><img src="/logo.png" alt="Logo"></a>' \
        '<a href="about.html"><span>About</span></a></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_relative_and_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo">' \
        '<img src="https://crawler-test.com/banner.png" alt="Banner"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/banner.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_missing_attributes(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="Logo">'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_many_attributes(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo" width="100" height="100">'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()