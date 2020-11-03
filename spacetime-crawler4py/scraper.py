import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

patternA = "((https?)://)?([\w_-]+)\.ics\.uci.edu/"
patternB = "((https?)://)?([\w_-]+)\.cs\.uci.edu/"
patternC = "((https?)://)?([\w_-]+)\.informatics\.uci.edu/"
patternD = "((https?)://)?([\w_-]+)\.stat\.uci.edu/"
patternE = "((https?)://)?([\w_-]+)\.today\.uci.edu/department/information_computer_sciences/"

visited_urls = set()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]
    #return extract_next_links(url, resp)

def extract_next_links(url, resp):
    soup = BeautifulSoup(resp.raw_response.content)
    links = []
    for link in soup.find_all("a"):
        if "href" in link.attrs:
            newurl = link.attrs["href"]
            if re.match(patternA, newurl) != None or re.match(patternB, newurl) != None or re.match(patternC, newurl) != None or re.match(patternD, newurl) != None or re.match(patternE, newurl) != None:
                links.append(newurl)
            #links.append(link.attrs["href"])
            
    print(newurl)
    return links

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise