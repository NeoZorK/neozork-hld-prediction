"""
Override the webbrowser module behavior inside Docker container
to show a URL message instead of trying to open a browser.
"""

def open(url, new=0, autoraise=True):
    """Dummy open function to replace webbrowser.open in Docker"""
    url_path = url.replace('file://', '')
    if '../results/plots' in url:
        # Extract just the filename from the URL/path
        import os
        filename = os.path.basename(url_path)
        print("\n\033[1;32m=== Plot is ready to view! ===\033[0m")
        print(f"\033[1;36mYou can view this plot in your browser at:\033[0m")
        print(f"\033[1;36m- http://localhost:8080/../plots/{filename} (if HTTP server is running)\033[0m")
        print(f"\033[1;36m- Or open directly from your host system at: ./../results/../plots/{filename}\033[0m")
    else:
        print(f"\n\033[1;33mCannot open browser in Docker container.\033[0m")
        print(f"\033[1;33mURL/file would be: {url_path}\033[0m")
    return True

def open_new(url):
    """Dummy open_new function to replace webbrowser.open_new in Docker"""
    return open(url, 1)

def open_new_tab(url):
    """Dummy open_new_tab function to replace webbrowser.open_new_tab in Docker"""
    return open(url, 2)
