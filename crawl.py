from urllib.parse import urlsplit

def normalize_url(url):
    """
    Normalize a URL by removing the scheme (http, https), port number, query parameters, and fragment.
    """
    split_url = urlsplit(url)
    if split_url.netloc.startswith("["):  # Check for port number and exclude IPv6 addresses
        netloc = split_url.netloc.split("]")[0] + "]"  # Keep the IPv6 address and remove the port
    elif ":" in split_url.netloc:  # Check for port number and exclude IPv4 addresses
        netloc = split_url.netloc.split(":")[0]  # Keep the domain and remove the port
    else:
        netloc = split_url.netloc
    path = split_url.path.rstrip('/')
    normalized_url = f"{netloc}{path}"
    return normalized_url

