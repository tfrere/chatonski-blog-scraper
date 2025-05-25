#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time
import argparse

def get_article_links_from_page(url):
    """Extract all article links from a blog page"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main blog posts list
        blog_posts = soup.find('ul', id='blog-posts-main')
        if not blog_posts:
            return [], None
        
        # Extract all article links in order
        links = []
        for a in blog_posts.find_all('a', href=True):
            if a['href'] not in links:  # Keep first occurrence only
                links.append(a['href'])
        
        # Find next page link if it exists
        next_page = None
        nav = soup.find('div', class_='nav-previous')
        if nav and nav.find('a'):
            next_page = nav.find('a')['href']
        
        return links, next_page
    except Exception as e:
        print(f"Error fetching page {url}: {str(e)}")
        return [], None

def extract_text_from_article(url):
    """Extract text content from an article page"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the article content
        article = soup.find('article', class_='post')
        if not article:
            return None
        
        # Get the title
        title = article.find('h1', class_='entry-title')
        title_text = title.get_text(strip=True) if title else "Sans titre"
        
        # Get the date
        date = article.find(class_='entry-date')
        date_text = date.get_text(strip=True) if date else "Date inconnue"
        
        # Remove unwanted elements
        for element in article.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        # Get text and clean it up
        content = article.get_text(separator='\n', strip=True)
        
        return {
            'title': title_text,
            'date': date_text,
            'url': url,
            'content': content
        }
    except Exception as e:
        print(f"Error fetching article {url}: {str(e)}")
        return None

def save_article(f, article):
    """Save a single article to the file"""
    f.write(f"=== {article['title']} ===\n")
    f.write(f"Date: {article['date']}\n")
    f.write(f"URL: {article['url']}\n\n")
    f.write(article['content'])
    f.write("\n\n---------\n\n")
    f.flush()  # Force write to disk

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Scrape articles from chatonsky.net')
    parser.add_argument('--limit', type=int, help='Limit the number of articles to process')
    args = parser.parse_args()

    start_url = "https://chatonsky.net/category/journal/"
    output_dir = "output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"chatonsky_articles_{timestamp}.txt")
    
    all_links = []
    current_url = start_url
    articles_needed = args.limit if args.limit else float('inf')
    
    print("Collecting article links...")
    while current_url and len(all_links) < articles_needed:
        links, next_page = get_article_links_from_page(current_url)
        all_links.extend(links)
        print(f"Found {len(links)} articles on {current_url}")
        
        if args.limit and len(all_links) >= args.limit:
            all_links = all_links[:args.limit]  # Trim to limit
            break
            
        current_url = next_page
        if next_page:
            time.sleep(0.5)  # Reduced delay
    
    print(f"\nProcessing {len(all_links)} articles...")
    
    # Open file for progressive saving
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, url in enumerate(all_links, 1):
            print(f"Processing article {i}/{len(all_links)}: {url}")
            article_data = extract_text_from_article(url)
            if article_data:
                save_article(f, article_data)
            time.sleep(0.5)  # Reduced delay
    
    print(f"Finished! Output saved to: {output_file}")

if __name__ == "__main__":
    main() 