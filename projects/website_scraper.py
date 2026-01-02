from bs4 import BeautifulSoup
import requests

# Standard headers to fetch a website
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# }

# A class to represent a Webpage
class Website:
    """
    A utility class to represent a Website that we have scraped
    """
    url: str
    title: str
    text: str

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        
        # Check if body exists before processing
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)#[:2_000]
        else:
            self.text = ""

    def __str__(self):
        """
        Return a string representation of this Website object
        """
        return f"Website(title={self.title}, url={self.url})"
    
if __name__ == "__main__":

    website = Website("https://edwarddonner.com")

    print(website)
    print(website.title)
    print(website.text)