import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

def web_scrape(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrive the website. Error: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # title
    title = soup.title.string if soup.title else 'No title found'
    print(f"\nWebsite Title: {title}")
    
    # headings h1,h2,h3
    headings = {
        'h1' : [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
        'h2' : [h2.get_text(strip=True) for h2 in soup.find_all('h2')],
        'h3' : [h3.get_text(strip=True) for h3 in soup.find_all('h3')]
    }
    print("\n")
    if headings:
        for level, texts in headings.items():
            for text in texts:
                print(f"{level.upper()} : {text}")
    else:
        print("\nHeading are not found")
    
    # paragraphs
    paragraphs = soup.find_all('p')
    print("\n")
    if paragraphs:
        for i, paragraph in enumerate(paragraphs, start=1):
            print(f"Paragraph {i}: {paragraph.get_text()}")
    else:
        print("Paragraphs are not found.")
        
    # images
    images = [{'alt' : img.get('alt',''), 'src': img['src']} for img in soup.find_all('img')]
    print("\n")
    if images:
        for img in images:
            print(f"ALT: {img['alt']}: SRC: {img['src']}")
    else:
        print("Images not found.")
        
    #tables
    tables = []
    for table in soup.find_all('table'):
        table_data = []
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if headers:
            table_data.append(headers)
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if(columns):
                table_data.append([column.get_text(strip=True) for column in columns])
            if table_data:
                tables.append(table_data)
        print("\nTables:")
        for table in tables:
            for row in table:
                print(row)
        ans = input("Do you want to save tables as CSV? (y/n): ")
        if (ans == 'y' or ans == 'Y'):
            save_tables(tables)
        
def save_tables(tables, folder='table'):
    if not os.path.exists(folder):
        os.mkdir(folder)
        
    for i, table in enumerate(tables):
        df = pd.DataFrame(table[1:], columns=table[0]) if len(table) > 1 else pd.DataFrame(table)
        table_name = os.path.join(folder, f"table_{i+1}.csv")
        df.to_csv(table_name, index=False)
        print(f"Table Saved: {table_name}")
            
if __name__ == "__main__":
    url = input("Enter the URL of the website to Scrape: ")
    if url.startswith("http://") or url.startswith("https://"):
        web_scrape(url)
    else:
        print("Enter URL which starts with 'http://' or 'https://'")