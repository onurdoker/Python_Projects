"""
Title: Continuous API Monitor

Subject: Time-based automation and API monitoring

Components: requests, time, csv (or Pandas)

Requirements:
- Fetch data from an external API (e.g. stock market data simulation)
- Create a loop that fetches data every 5 minutes using time.sleep()
- Continuously append fetched data along with its timestamp to a simple CSV file named 'log.csv'.
"""

import os
import requests
import time
import csv
from datetime import datetime


API_KEY = "f2ff59b4af76aede47a930deb084efae"
SYMBOL = "AAPL"
BASE_URL = "http://api.marketstack.com/v2/eod"

current_dir = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(current_dir, "log.csv")


def fetch_stock_data(symbol):
    params = {"access_key": API_KEY, "symbols": symbol, "limit": 1}

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return data["data"][0]
    else:
        return None


def append_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "date", "close"])
        writer.writerow(
            [
                datetime.now(),
                data.get("symbol"),
                data.get("date"),
                data.get("close"),
            ]
        )


def main():
    while True:
        try:
            stock_data = fetch_stock_data(SYMBOL)
            if stock_data:
                append_to_csv(log_file_path, stock_data)
                print(
                    f"Data fetched successfully for {stock_data['symbol']} at {datetime.now()}"
                )
            else:
                print(f"Failed to fetch data for {SYMBOL}")
        except Exception as error:
            print(f"Error fetching or logging data: {error}")

        time.sleep(300)


if __name__ == "__main__":
    main()
