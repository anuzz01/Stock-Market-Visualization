import requests
import json
import csv
import sys
import datetime

def transform_to_csv():
    """
    Transforming pulled data to csv file
    loop through stocks - for each:
      build file name
      read json data from that file name
      loop through json data for each line of data:
        append to new csv file
    """

    stocks = ["GOOGL", "FB","AMZN","NFLX"]
    data_folder = "./data/"
    filename = data_folder + "all_stocks.csv"
    file_handler = csv.writer(open(filename, "w"))

    # Write CSV Header, If you dont need that, remove this line
    file_handler.writerow(["Date", "Open", "High", "Low", "Close","Stock"])

    for stock in stocks:
        with open(data_folder + stock + ".json") as json_file:
            output_json = json.load(json_file)
            for x in output_json["prices"]:
                date = datetime.datetime.fromtimestamp(x["date"]).strftime('%Y-%m-%d')
                file_handler.writerow([
                            date,
                            x["open"],
                            x["high"],
                            x["low"],
                            x["close"],
                            stock])





























#stock loop
