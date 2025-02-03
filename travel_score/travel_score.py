import pandas as pd
from geopy.geocoders import Nominatim
from typing import Tuple, Dict, Set, Optional
import collections
import logging
import os
import csv
import argparse
import sys

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_coordinates_from_db(city: str, country: str, city_db_path: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Get latitude and longitude from the database.

    Args:
        city (str): Name of the city
        country (str): Name of the country
        city_db_path (str): Path to the city database CSV file

    Returns:
        Tuple[Optional[float], Optional[float]]: Latitude and longitude if found
    """
    try:
        with open(city_db_path, 'r') as csvfile:
            lines = csv.reader(csvfile)
            for line in lines:
                if line[0].strip() == city and line[1].strip() == country:
                    logging.info(f"Found coordinates for {city}, {country} in database")
                    return float(line[3]), float(line[4])
    except FileNotFoundError:
        logging.warning(f"City database file not found: {city_db_path}")
    return None, None

def get_coordinates_from_geopy(city: str, country: str) -> Tuple[float, float]:
    """Get coordinates using geopy service"""
    logging.info(f"Fetching coordinates for {city}, {country} from geopy")
    user_agent = os.getenv('GEOLOCATOR_USER_AGENT', 'travel_score_app')
    geolocator = Nominatim(user_agent=user_agent)
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
        raise ValueError(f"Could not find coordinates for {city}, {country}")
    except Exception as e:
        logging.error(f"Geopy error for {city}, {country}: {str(e)}")
        raise

def update_city_db(city: str, country: str, lat: float, lon: float, city_db_path: str) -> None:
    """Add new coordinates to the city database"""
    with open(city_db_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([city.strip(), country.strip(), lat, lon])
    logging.info(f"Added coordinates for {city}, {country} to database")

def process_city_coordinates(input_path: str, city_db_path: str, output_path: str) -> None:
    """
    Process city coordinates from input CSV and generate JSON output with location data.
    
    Args:
        input_path (str): Path to input CSV file with cities
        city_db_path (str): Path to city database
        output_path (str): Path for output JSON file
    """
    # Read input CSV file
    try:
        df = pd.read_csv(input_path)
        required_columns = {'City', 'Country'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Input file must contain columns: {required_columns}")
    except Exception as e:
        logging.error(f"Error reading input file: {str(e)}")
        sys.exit(1)

    # Process each city
    results = []
    for _, row in df.iterrows():
        city, country = row['City'].strip(), row['Country'].strip()
        
        # Try database first
        lat, lon = get_coordinates_from_db(city, country, city_db_path)
        
        # If not in database, use geopy
        if lat is None or lon is None:
            try:
                lat, lon = get_coordinates_from_geopy(city, country)
                update_city_db(city, country, lat, lon, city_db_path)
            except Exception as e:
                logging.error(f"Skipping {city}, {country}: {str(e)}")
                continue
        
        results.append({
            'City': city,
            'Country': country,
            'Latitude': lat,
            'Longitude': lon
        })

    # Save results to JSON
    try:
        df_results = pd.DataFrame(results)
        df_results.to_json(output_path, orient='records', indent=2)
        logging.info(f"Successfully processed {len(results)} cities")
        logging.info(f"Results saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving results: {str(e)}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Process city coordinates and generate JSON output')
    parser.add_argument('--input_file', help='Input CSV file containing City and Country columns')
    parser.add_argument('--citydb', default='city_database.csv', 
                      help='City database CSV file (default: city_database.csv)')
    parser.add_argument('--output', default='travel_data.json',
                      help='Output JSON file path (default: travel_data.json)')
    
    args = parser.parse_args()
    
    setup_logging()
    process_city_coordinates(args.input_file, args.citydb, args.output)

if __name__ == '__main__':
    main()
