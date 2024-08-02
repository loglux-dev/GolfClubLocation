"""
Author: Vladislav Sorokin
Email: call2vlad@outlook.com
Upwork Profile: https://www.upwork.com/freelancers/~019599c21a583c9cb7
Date Created: 2/08/2024
Last Updated: 2/08/2024
Description: This script scrapes golf club information from the Golfriket website,
including club names, coordinates, URLs, and addresses, and saves the data into a CSV file.
License: MIT License
"""

import requests
from bs4 import BeautifulSoup
import re
import ast
import csv


class GolfClub:
    """Class representing a golf club."""

    def __init__(self, name, latitude, longitude, url_path, base_url):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.url = base_url + url_path
        self.address = None

    def fetch_address(self):
        """Fetch the address details from the golf club's page."""
        try:
            print(f"Fetching address for {self.name} from {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()
            page_soup = BeautifulSoup(response.content, 'html.parser')

            address_divs = page_soup.find_all('div')
            address = ""
            for div in address_divs:
                if "float:left;width:80px" in div.get('style', ''):
                    key = div.get_text(strip=True)
                    value_div = div.find_next_sibling('div')
                    value = value_div.get_text(strip=True) if value_div else ""
                    address += f"{key}: {value}, "
            self.address = address.strip(', ')
            print(f"Address for {self.name}: {self.address}")
        except requests.exceptions.RequestException as e:
            self.address = "Address not found"
            print(f"Failed to fetch address for {self.name}: {e}")


class GolfClubScraper:
    """Class to scrape golf club information from the website."""

    def __init__(self, base_url, main_url):
        self.base_url = base_url
        self.main_url = main_url
        self.clubs = []

    def scrape(self):
        """Scrape the golf club data and store it in self.clubs."""
        try:
            print(f"Fetching main page: {self.main_url}")
            response = requests.get(self.main_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')

            locations = self.extract_locations(scripts)
            if locations:
                print(f"Found {len(locations)} clubs in the script.")
                self.process_locations(locations)
            else:
                print("Could not find the locations array in the script.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")

    def extract_locations(self, scripts):
        """Extract the locations array from the scripts."""
        for script in scripts:
            if script.string and 'var locations =' in script.string:
                pattern = r'var\s+locations\s*=\s*(\[.*?\]);'
                match = re.search(pattern, script.string, re.DOTALL)
                if match:
                    locations_code = match.group(1)
                    locations = ast.literal_eval(locations_code)
                    print("Extracted locations array from script.")
                    return locations
        print("Locations array not found in scripts.")
        return None

    def process_locations(self, locations):
        """Create GolfClub instances for each location."""
        for location in locations:
            club_name = location[0]
            latitude = location[1]
            longitude = location[2]
            url_path = location[4]

            club = GolfClub(club_name, latitude, longitude, url_path, self.base_url)
            club.fetch_address()
            self.clubs.append(club)

    def save_to_csv(self, filename='golf_clubs.csv'):
        """Save the scraped data to a CSV file."""
        print(f"Saving data to {filename}")
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Club', 'Latitude', 'Longitude', 'URL', 'Address']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for club in self.clubs:
                writer.writerow({
                    'Club': club.name,
                    'Latitude': club.latitude,
                    'Longitude': club.longitude,
                    'URL': club.url,
                    'Address': club.address
                })
                print(f"Saved club: {club.name}")


if __name__ == "__main__":
    base_url = "https://www.golfriket.se"
    main_url = base_url + '/golfklubbar/'

    scraper = GolfClubScraper(base_url, main_url)
    scraper.scrape()
    scraper.save_to_csv()
