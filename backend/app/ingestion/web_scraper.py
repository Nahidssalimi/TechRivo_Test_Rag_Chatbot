"""
Web scraping utilities for ingesting company website content
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Set
from urllib.parse import urljoin, urlparse
import time


class WebScraper:
    """Scrapes and extracts text content from websites"""
    
    def __init__(self, max_pages: int = 50, delay: float = 1.0):
        """
        Args:
            max_pages: Maximum number of pages to scrape per domain
            delay: Delay between requests in seconds (be polite!)
        """
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls: Set[str] = set()
    
    def scrape_url(self, url: str) -> Dict[str, any]:
        """
        Scrape a single URL and extract text content
        
        Returns:
            Dict with content and metadata
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
    
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
         
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
               
                text = main_content.get_text(separator='\n', strip=True)
             
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                content = '\n'.join(lines)
                
                return {
                    'content': content,
                    'metadata': {
                        'source': url,
                        'title': title_text,
                        'type': 'webpage',
                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
            
            return None
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def get_links(self, url: str, base_domain: str) -> List[str]:
        """
        Extract all internal links from a page
        Only returns links within the same domain
        """
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                
        
                absolute_url = urljoin(url, href)
                
             
                if urlparse(absolute_url).netloc == base_domain:
                 
                    clean_url = absolute_url.split('#')[0].split('?')[0]
                    if clean_url and clean_url not in links:
                        links.append(clean_url)
            
            return links
            
        except Exception as e:
            print(f"Error getting links from {url}: {str(e)}")
            return []
    
    def scrape_website(self, start_url: str, follow_links: bool = True) -> List[Dict[str, any]]:
        """
        Scrape a website starting from a URL
        Optionally follows internal links up to max_pages
        
        Args:
            start_url: Starting URL to scrape
            follow_links: Whether to follow internal links
            
        Returns:
            List of document dicts with content and metadata
        """
        documents = []
        self.visited_urls = set()
        

        parsed = urlparse(start_url)
        base_domain = parsed.netloc
        
       
        to_visit = [start_url]
        
        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            print(f"Scraping: {url}")
            self.visited_urls.add(url)
            
           
            doc = self.scrape_url(url)
            if doc and doc['content'].strip():
                documents.append(doc)
            
            
            if follow_links and len(self.visited_urls) < self.max_pages:
                links = self.get_links(url, base_domain)
                for link in links:
                    if link not in self.visited_urls and link not in to_visit:
                        to_visit.append(link)
            
         
            time.sleep(self.delay)
        
        print(f"Scraped {len(documents)} pages from {base_domain}")
        return documents
    
    def scrape_sitemap(self, sitemap_url: str) -> List[Dict[str, any]]:
        """
        Scrape URLs from a sitemap.xml file
        Useful for comprehensive site coverage
        """
        documents = []
        
        try:
            response = requests.get(sitemap_url, timeout=10)
            soup = BeautifulSoup(response.text, 'xml')
            
            urls = [loc.text for loc in soup.find_all('loc')]
            
            print(f"Found {len(urls)} URLs in sitemap")
            
            for url in urls[:self.max_pages]:
                if url not in self.visited_urls:
                    print(f"Scraping from sitemap: {url}")
                    self.visited_urls.add(url)
                    
                    doc = self.scrape_url(url)
                    if doc and doc['content'].strip():
                        documents.append(doc)
                    
                    time.sleep(self.delay)
            
        except Exception as e:
            print(f"Error scraping sitemap {sitemap_url}: {str(e)}")
        
        return documents
