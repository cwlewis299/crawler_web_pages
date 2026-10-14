import asyncio
import sys
from crawl import crawl_site_async

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    else:
        base_url = sys.argv[1]
        max_concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        print(f"starting crawl of: {base_url}")
        try:
            page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
            #print(f"\nCrawl completed for: {base_url}\n{page_data}")
            for data in page_data.values():
                #print(f"\nURL: {url}")
                print(f"\nHeading: {data['heading']}")
                print(f"-First Paragraph: {data['first_paragraph']}")
                #print(f"Outgoing Links: {data['outgoing_links']}")
                #print(f"Image URLs: {data['image_urls']}")
                
            print(f"\nTotal pages crawled: {len(page_data)}")
        except Exception as e:
            print(f"Error occurred while fetching HTML: {e}")
            sys.exit(1)

        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
