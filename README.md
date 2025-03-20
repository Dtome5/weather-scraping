# Weather Data Scraper 

This project provides a framework for collecting, storing, and visualizing weather data from multiple locations. It automates data extraction using web scraping and APIs, stores the results in an HDF5 file, and generates informative visualizations of key weather parameters.

---

## Features

- **Data Collection**: Automates the retrieval of weather data (temperature, humidity, and wind speed) from the OpenWeather platform.
- **Data Storage**: Organizes and stores data hierarchically in an HDF5 file for efficient access and scalability.
- **Visualization**: Creates plots to analyze trends across locations and parameters, aiding in comparative analysis.

---

## Requirements

Ensure the following dependencies are installed:

- Python 3.x
- `requests`
- `h5py`
- `pandas`
- `matplotlib`
- `bs4` (BeautifulSoup)
- `requests_cache`
- `openmeteo_requests`
- `numpy`
- `retry_requests`

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## Files Overview

1. **`websites.csv`**:  
   Contains the list of URLs and locations to scrape weather data.

2. **`extract.py`**:  
   A script to scrape weather data, retrieve historical data using the Open-Meteo API, and store results in an HDF5 file.

3. **`viz.py`**:  
   A script to generate visualizations of weather trends for each parameter and location.

---

## Usage

### 1. Data Extraction
Run the `extract.py` script to scrape weather data and save it to the `weather.hdf5` file:
```bash
python extract.py
```

### 2. Visualization
Run the `viz.py` script to generate plots based on the stored data:
```bash
python viz.py
```

Generated plots will be saved in the current directory.

---

## Setting Up the Cron Job

Automate the data collection process by setting up a cron job. Here's how:

1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add the following line to schedule the `extract.py` script to run daily at midnight:
   ```bash
   0 12 * * * ~/run.sh
   ```

Replace `/path/to/run.sh` with the full path to the script.

3. Save and exit the editor. The cron job is now set to run daily.

---

## Known Limitations

- **Error Handling**: Currently, the scraping scripts lack robust error-handling mechanisms for dynamic content and unexpected webpage changes.
---


