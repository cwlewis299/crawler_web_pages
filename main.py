import sys
from crawl import get_html

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    else:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")
        try:
            print(f"{get_html(base_url)}")
        except Exception as e:
            print(f"Error occurred while fetching HTML: {e}")
            sys.exit(1)

        sys.exit(0)


if __name__ == "__main__":
    main()
