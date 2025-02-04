# Travel Score JSON Generator

A Python tool that processes city data and generates JSON output with geographical coordinates. The tool uses local caching to minimize API calls and provides both command-line and programmatic interfaces.

## Features

- Convert city/country pairs to geographical coordinates
- Local caching of coordinates in CSV database
- Fallback to Nominatim geocoding service when coordinates aren't cached
- JSON output with standardized location data
- Robust error handling and logging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel_score_json.git
cd travel_score_json
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the package and dependencies:
```bash
pip install -e .
```

## Usage

### Command Line Interface

Basic usage with default options:
```bash
python -m travel_score.travel_score --input_file cities.csv
```

Full options:
```bash
python -m travel_score.travel_score \
    --input_file cities.csv \
    --citydb custom_database.csv \
    --output custom_output.json
```

### Input File Format

The input CSV file must contain at least these columns:
- `City`: Name of the city
- `Country`: Name of the country

Example `cities.csv`:
```csv
City,Country
Paris,France
Tokyo,Japan
New York,United States
```

### Environment Variables

- `GEOLOCATOR_USER_AGENT`: Custom user agent for Nominatim geocoding service (default: 'travel_score_app')

### Output

The tool generates a JSON file containing an array of objects with the following structure:
```json
[
  {
    "City": "Paris",
    "Country": "France",
    "Latitude": 48.8566,
    "Longitude": 2.3522
  }
]
```

## Development

### Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

### Setting Up Development Environment

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- Uses [Nominatim](https://nominatim.org/) for geocoding services
- Built with [pandas](https://pandas.pydata.org/) for data processing
