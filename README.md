# Golf Club Location Scraper

This project is a web scraper built to extract detailed information about golf clubs in Sweden from the [Golfriket website](https://www.golfriket.se). The scraper collects data on each club's name, latitude, longitude, URL, and address, and exports this information into a CSV file for analysis and usage.

## Features

- **Scrapes Golf Club Information**: Collects data such as the club name, latitude, longitude, URL, and physical address.
- **CSV Export**: Saves the scraped data into a CSV file for easy access and analysis.
- **Error Handling**: Includes basic error handling for network requests and parsing operations.
- **Class-Based Design**: Utilizes a class-based approach for improved organization and maintainability of the code.

## Installation

To set up and run this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/loglux/GolfClubLocation.git
    ```
   
2. **Navigate to the project directory**:
    ```bash
    cd GolfClubLocation
    ```
3 **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the scraper**:
    ```bash
   python golf_club_scraper.py
    ```
This will generate a golf_clubs.csv file in the current directory containing the extracted data.

Code Structure
- GolfClub class: Represents a golf club and contains methods to fetch its address details.
- GolfClubScraper class: Manages the scraping process, including fetching and parsing data from the main page and individual club pages

License
This project is licensed under the MIT License - see the LICENSE file for details.