import asyncio
from types import TracebackType
from urllib.parse import urlsplit, urljoin
from typing import TypedDict

import aiohttp
from bs4 import BeautifulSoup


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

class AsyncCrawler:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.base_domain = self.get_base_domain(base_url)
        self.page_data: dict[str, PageData] = {}
        self.visited: set[str] = set()
        self.lock = asyncio.Lock()
        self.max_concurrency: int = 5  # Limit the number of concurrent requests
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None
        self.max_pages: int = 100  # Limit the number of pages to crawl

    def get_base_domain(self, url: str) -> str:
        """
        Extract the base domain from the given URL.
        """
        split_url = urlsplit(url)
        if split_url.netloc.startswith("["):  # Check for port number and exclude IPv6 addresses
            netloc = split_url.netloc.split("]")[0] + "]"  # Keep the IPv6 address and remove the port
        elif ":" in split_url.netloc:  # Check for port number
            netloc = split_url.netloc.split(":")[0]  # Keep the domain and remove the port
        else:
            netloc = split_url.netloc
        return netloc

    async def __aenter__(self) -> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
            self, 
            exc_type: type[BaseException] | None, 
            exc_val: BaseException | None, 
            exc_tb: TracebackType | None,
        ) -> None:
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        """
        Add a normalized URL to the visited set in a thread-safe manner.
        """
        #print(f"Adding page visit for: {normalized_url}")
        async with self.lock:
            if normalized_url in self.visited:
                return False  # URL has already been visited
            self.visited.add(normalized_url)
            #print(f"Visited URLs: {self.visited}")
            return True  # URL added successfully

    async def get_html(self, url: str) -> str | None:
        """
        Fetches the HTML content of the given URL and returns it as a string.
        If an error occurs, raises an error
        """
        if self.session is None:
            return None  # Session is not initialized
        
        #print(f"ATTEMPTING to fetch HTML for: {url}")
        try:
            async with self.session.get(
                url, headers={'User-Agent': "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.3"}
                ) as response:

                #print(f"***Response status: {response.status} for URL: {url}")
                if response.status > 399:
                    print(f"Error: HTTP error {response.status} for URL: {url}")
                    return None  # Return None if the response status is an error
                
                #print(f"{response.headers}")
                #print(f"***Content-Type: {response.headers.get('Content-Type')} for URL: {url}")
                if 'text/html' not in response.headers['Content-Type']:
                    print(f"Error: URL {url} did not return HTML content. Content-Type: {response.headers['Content-Type']}")
                    return None  # Return None if the content is not HTML
                
                #print(f"***GOT HTML for: {url} (length: {len(await response.text())})")  # Print the length of the HTML for debugging
                return await response.text() 
            
        except Exception as e:
            #print(f"OMG we had an error in get_html)")
            print(f"Error occurred while fetching HTML from {url}: {e}")
            return None  # Return None if an exception occurs

    async def crawl_page(self, current_url: str=None) -> None:
        """
        Crawls the given base URL and extracts the page data for each page found.
        The method is recursive and will continue to crawl outgoing links until all pages have been visited or the maximum number of pages has been reached.
        Mutates the page_data dictionary with the extracted data for each page.
        Prints active crawling statements and any skipped pages.
        """
        #print(f"Started crawl_page method for: {current_url if current_url else self.base_url}")

        if current_url is None:
            current_url = self.base_url

        normalized_current_url = normalize_url(current_url)
        normalized_base_url = normalize_url(self.base_url)

        #print(f"Normalized current URL: {normalized_current_url}")

        # Check if the current URL is within the base URL's domain
        if normalized_base_url not in normalized_current_url:
            return
        
        # Call and await add_page_visit to check if the URL has already been visited
        if not await self.add_page_visit(normalized_current_url):
            return

        #print(f"Visiting URL: {current_url}")

        async with self.semaphore:  # Limit the number of concurrent requests
            try:
                print(
                    f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value}/{self.max_concurrency})"
                )
                html = await self.get_html(current_url)
                if html is None:
                    print(f"Error: No HTML to fetch for {current_url}. Skipping this page.")
                    return
                #print(f"***FETCHED HTML: {len(html)}...")  # Print the first 100 characters of the HTML for debugging
                extract_data = extract_page_data(html, current_url)
            except Exception as e:
                print(f"Error occurred while crawling {current_url}: {e}")
            
        async with self.lock:
            #print(f"LOCKED and adding page data for: {normalized_current_url} with data")
            self.page_data[normalized_current_url] = extract_data
            #print(f"Page data added for: {normalized_current_url}. Total pages crawled so far: {len(self.page_data)}")

        outgoing_links = self.page_data[normalized_current_url]["outgoing_links"]
        tasks = []
        for link in outgoing_links:
            #print(f"CRAWLING LINK: {link}")
            tasks.append(asyncio.create_task(self.crawl_page(link)))  # Recursively crawl the outgoing links
            #print(f"Created task for link: {link}")
        await asyncio.gather(*tasks)  # Wait for the task to complete
        #print("Completed TASKS")
            #crawl_page(base_url, link, page_data) # Recursively crawl the outgoing links
            

    async def crawl(self) -> dict[str, PageData]:
        """
        Starts the crawling process from the base URL.
        Returns a dictionary containing the extracted data for each page.
        """
        #print(f"Started crawl function for: {self.base_url}")
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url: str) -> dict[str, PageData]:
    """
    Asynchronously crawls the given base URL and returns a dictionary containing the extracted data for each page.
    """
    async with AsyncCrawler(base_url) as crawler:
        #print(f"Started AsyncCrawler of: {base_url}")
        return await crawler.crawl()

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

"""def get_html(url: str) -> str:
    
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
        raise RuntimeError(f"Error occurred while fetching HTML from {url}: {e}")"""

"""def crawl_page(base_url: str, current_url: str=None, page_data: dict[str, PageData]=None):
    
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
        print(f"Error occurred while crawling {current_url}: {e}")"""