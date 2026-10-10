from urllib.parse import urlsplit, urljoin
from typing import TypedDict
from bs4 import BeautifulSoup
import requests

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url):
    """
    Normalize a URL by removing the scheme (http, https), port number, query parameters, and fragment.
    """
    split_url = urlsplit(url)
    if split_url.netloc.startswith("["):  # Check for port number and exclude IPv6 addresses
        netloc = split_url.netloc.split("]")[0] + "]"  # Keep the IPv6 address and remove the port
    elif ":" in split_url.netloc:  # Check for port number
        netloc = split_url.netloc.split(":")[0]  # Keep the domain and remove the port
    else:
        netloc = split_url.netloc
    path = split_url.path.rstrip('/')
    normalized_url = f"{netloc}{path}"
    return normalized_url

def get_heading_from_html(html: str) -> str:
    """
    Extract the first heading (h1 or h2) from the given HTML string.
    If no heading is found, return an empty string.
    """
    soup = BeautifulSoup(html, 'html.parser')
    heading1 = soup.find('h1')
    if heading1:
        return heading1.get_text(strip=True)
    heading2 = soup.find('h2')
    if heading2:
        return heading2.get_text(strip=True)
    return ""

def get_first_paragraph_from_html(html: str) -> str:
    """
    Extract the main or first paragraph (p) from the given HTML string.
    If no paragraph is found, return an empty string.
    """
    soup = BeautifulSoup(html, 'html.parser')
    main_tag = soup.find('main')
    if main_tag:
        first_paragraph = main_tag.find('p')
        if first_paragraph:
            return first_paragraph.get_text(strip=True)
    first_paragraph = soup.find('p')
    if first_paragraph:
        return first_paragraph.get_text(strip=True)
    return ""

def get_urls_from_html(html: str, base_url: str) -> list[str] | str:
    """
    Extract all URLs from the given HTML string and returns an 
    un-normalized list of all the URLs found within the HTML, and 
    an error if one occurs.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            urls.append(urljoin(base_url, href))
        return urls
    except Exception as e:
        return f"Error occurred while parsing HTML: {e}"

def get_images_from_html(html, base_url):
    """
    Extract all image URLs from the given HTML 
    string and returns an un-normalized list of all the image URLs 
    found within the HTML, and an error if one occurs
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        image_urls = []
        for img_tag in soup.find_all('img', src=True):
            src = img_tag['src']
            image_urls.append(urljoin(base_url, src))
        return image_urls
    except Exception as e:
        return f"Error occurred while parsing HTML: {e}"


def extract_page_data(html: str, page_url: str) -> PageData:
    """
    Extracts the URLs, heading, first paragraph, outgoing links, and image URLs from 
    the given HTML string and returns a dictionary containing the extracted data.
    """
    dict_data = {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
    return dict_data

def get_html(url: str) -> str:
    """
    Fetches the HTML content of the given URL and returns it as a string.
    If an error occurs, raises an error
    """
    try:
        response = requests.get(url, headers={'User-Agent': "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.3"})
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        #print(f"{response.headers}")
        if 'text/html' not in response.headers['Content-Type']:
            raise RuntimeError(f"URL {url} did not return HTML content.")
        return response.text
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error occurred while fetching HTML from {url}: {e}")

def crawl_page(base_url: str, current_url: str=None, page_data: dict[str, PageData]=None):
    """
    Crawls the given base URL and extracts the page data for each page found.
    Returns a dictionary containing the extracted data for each page.
    """
    if page_data is None:
        page_data = {}

    if current_url is None:
        current_url = base_url

    normalized_current_url = normalize_url(current_url)
    normalized_base_url = normalize_url(base_url)

    # Check if the current URL is within the base URL's domain
    if normalized_base_url not in normalized_current_url:
        return page_data

    # Check if the current URL has already been crawled
    if normalized_current_url in page_data:
        return page_data

    try:
        html = get_html(current_url)
        page_data[normalized_current_url] = extract_page_data(html, current_url)
        outgoing_links = page_data[normalized_current_url]["outgoing_links"]

        for link in outgoing_links:
            print(f"Crawling link: {link}")
            crawl_page(base_url, link, page_data) # Recursively crawl the outgoing links
        return page_data
    except Exception as e:
        print(f"Error occurred while crawling {current_url}: {e}")