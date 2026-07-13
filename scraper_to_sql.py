import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3  # Imported our database engine

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    print(f"Failed to connect to {url}. Status code: {response.status_code}")
    return None

def parse_books(html_content, all_books_list):
    soup = BeautifulSoup(html_content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    print(f"-> Found {len(books)} books on this page.")
    
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        # Clean the text price string (e.g., '£51.77') into a pure database float number
        price_cleaned = float(price_text.replace("£", "").replace("Â", ""))
        availability = book.find("p", class_="instock availability").text.strip()
        
        book_data = {
            "Title": title,
            "Price": price_cleaned,
            "Availability": availability
        }
        all_books_list.append(book_data)

def save_to_database(book_list):
    database_name = "scraped_marketplace.db"
    
    # Establish pipe connection and cursor pointer
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Architect the relational data schema rules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            availability TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    print(f"\nStreaming {len(book_list)} rows into relational database columns...")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Programmatically pipe each scraped row dictionary into the SQL schema table
    for book in book_list:
        cursor.execute("""
            INSERT INTO scraped_books (title, price, availability, timestamp)
            VALUES (?, ?, ?, ?)
        """, (book["Title"], book["Price"], book["Availability"], current_time))
        
    conn.commit()
    conn.close()
    print(f"✅ Success! Database transaction sealed completely inside '{database_name}'.")

if __name__ == "__main__":
    master_book_list = []
    
    target_urls = [
        "https://books.toscrape.com",
        "http://books.toscrape.com/catalogue/page-2.html",
        "http://books.toscrape.com/catalogue/page-3.html"
    ]
    
    try:
        page_count = 1
        for current_url in target_urls:
            print(f"Scraping Page {page_count}: {current_url}")
            html = fetch_page(current_url)
            if html:
                parse_books(html, master_book_list)
            page_count += 1
                
        print(f"\nExtraction complete! Harvested a total of {len(master_book_list)} assets.")
        
        # Trigger our new relational database pipeline engine
        save_to_database(master_book_list)
        
    except Exception as e:
        print(f"Pipeline crashed. Reason: {str(e)}")
