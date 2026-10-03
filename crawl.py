from urllib.parse import urlsplit

def normalize_url(url):
    split_url = urlsplit(url)
    if ":" in split_url.netloc and "[" not in split_url.netloc:  # Check for port number and exclude IPv6 addresses]":
        netloc = split_url.netloc.split(":")[0]
    else:
        netloc = split_url.netloc
    path = split_url.path.rstrip('/')
    normalized_url = f"{netloc}{path}"
    return normalized_url