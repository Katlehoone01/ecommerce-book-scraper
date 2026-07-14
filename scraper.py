import csv
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        
        book_data = {
            "Title": title,
            "Price": price,
            "Availability": availability
        }
        all_books_list.append(book_data)

if __name__ == "__main__":
    master_book_list = []
    
    # Track execution start in the log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("pipeline.log", mode="a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] PIPELINE STARTED: Running static array parser.\n")
    print("Pipeline initialized...")
    
    # Explicit, direct server endpoints to guarantee zero formatting errors
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
                
        print(f"\nExtraction complete! Extracted a total of {len(master_book_list)} books.")
        
        # Write clean data to the spreadsheet file
        csv_filename = "books.csv"
        fieldnames = ["Title", "Price", "Availability"]
        
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(master_book_list)
            
        # Log ultimate pipeline success status
        success_message = f"SUCCESS: Extracted {len(master_book_list)} books and updated '{csv_filename}'."
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("pipeline.log", mode="a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] {success_message}\n")
        print(f"Log updated: {success_message}")
        
    except Exception as e:
        error_message = f"ERROR: Pipeline crashed. Reason: {str(e)}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("pipeline.log", mode="a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] {error_message}\n")
        print(f"Log updated: {error_message}")
