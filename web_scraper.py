import csv
import requests
from bs4 import BeautifulSoup
import os

def scrape_local_html(filepath='mock_products.html'):
    """
    Scrapes product information from a local HTML file.

    Args:
        filepath (str): The path to the local HTML file.

    Returns:
        list: A list of lists, where each inner list contains the
              name, price, and rating of a product.
    """
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        print("Please make sure 'mock_products.html' is in the same directory as the script.")
        return []

    print(f"Reading and parsing local file: {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    products_data = []
    # Find all product containers using the 'product-card' class
    # This class is defined in our 'mock_products.html' file
    product_containers = soup.find_all('div', class_='product-card')

    if not product_containers:
        print("No products found. Did you change the 'product-card' class in the HTML?")
        return []

    print(f"Found {len(product_containers)} products. Extracting details...")
    for product in product_containers:
        try:
            # Extract product name using the 'product-name' class
            name_element = product.find('h3', class_='product-name')
            name = name_element.text.strip() if name_element else 'N/A'

            # Extract product price using the 'product-price' class
            price_element = product.find('p', class_='product-price')
            price = price_element.text.strip() if price_element else 'N/A'

            # Extract product rating using the 'product-rating' class
            # This is designed to fail gracefully if the rating is not present
            rating_element = product.find('div', class_='product-rating')
            if rating_element:
                # We'll grab the more descriptive text part of the rating
                rating = rating_element.find('span', class_='text-gray-600').text.strip()
            else:
                rating = 'N/A' # Handle products with no rating

            if name != 'N/A':
                products_data.append([name, price, rating])

        except AttributeError as e:
            # This is a fallback for unexpected missing elements
            print(f"Skipping a product due to a missing attribute: {e}")
            continue

    return products_data

def save_to_csv(data, filename='products_scraped_data.csv'):
    """
    Saves the scraped product data to a CSV file.

    Args:
        data (list): The list of product data to save.
        filename (str): The name of the output CSV file.
    """
    if not data:
        print("No data to save.")
        return

    print(f"Saving data to {filename}...")
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['Product Name', 'Price', 'Rating'])
            # Write the product data
            writer.writerows(data)
        print(f"Successfully saved {len(data)} products to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

if __name__ == '__main__':
    # --- Main Execution ---

    # 1. Scrape the data from the local HTML file
    scraped_data = scrape_local_html('mock_products.html')

    # 2. Save the data to a CSV file
    if scraped_data:
        save_to_csv(scraped_data)

