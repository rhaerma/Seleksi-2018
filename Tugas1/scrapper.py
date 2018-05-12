import urllib3
import scrape_myfave as fave
from bs4 import BeautifulSoup

# Get Raw Source
def getSource(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'))
    return soup

if __name__ == "__main__":
    url = "https://myfave.com/bandung/bestdeal"
    soup = getSource(url)
    #soup = BeautifulSoup("<script>foo<bar>baz</script>")
    print(soup)