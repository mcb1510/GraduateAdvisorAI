import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_all_faculty_urls():
    """Get all faculty profile URLs from the main faculty page"""
    base_url = "https://www.boisestate.edu/coen-cs/people/faculty/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    faculty_urls = []
    
    # Find all links that contain faculty profile URLs
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/people/faculty/' in href and href != base_url:
            if href.startswith('/'):
                href = 'https://www.boisestate.edu' + href
            faculty_urls.append(href)
    
    # Remove duplicates
    faculty_urls = list(set(faculty_urls))
    return faculty_urls

# Test
# faculty_urls = get_all_faculty_urls()
# print(f"Found {len(faculty_urls)} faculty URLs:")
# for url in faculty_urls:
#     print(url)

def scrape_faculty(url):
    """Improved version of your scraping function"""
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # Name
        name = soup.find("h1").text.strip() if soup.find("h1") else "Unknown"
        
        # Email
        email_elem = soup.select_one("a[href^='mailto:']")
        email = email_elem.text.strip() if email_elem else None
        
        # Research areas - look in multiple places
        research = ""
        for heading in soup.find_all(["h2", "h3", "strong"]):
            if "research" in heading.text.lower() or "interests" in heading.text.lower():
                next_p = heading.find_next("p")
                if next_p:
                    research = next_p.text.strip()
                    break
        
        # Bio/Summary - get main content
        bio = ""
        content_div = soup.find("div", class_="wp-block-post-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            if paragraphs:
                bio = paragraphs[0].text.strip()

        return {
            "Name": name,
            "Email": email,
            "Research_Areas": research,
            "Bio": bio,
            "URL": url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
faculty_urls = get_all_faculty_urls()
data = scrape_faculty(faculty_urls[0])
print(data)