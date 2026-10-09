from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag # type: ignore

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

#def get_images_from_html(html, base_url):
    """
    Extract all image URLs from the given HTML 
    string and returns an un-normalized list of all the image URLs 
    found within the HTML, and an error if one occurs
    """
 #   pass