import requests
import json
import sys

def get_stock_data():
    """
    Getting all data
    list of stocks
    loop through the stocks - for each:
      build new url for each stock
      do get call using that url
      save each returned answer in json file
    """

    #forming url to get historical data
    host_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/"
    end_point_historic = "stock/v3/get-historical-data?"
    common_parameter = "period1=1483228800&period2=1575776492"

    #api key using this method so that it is not public
    api_key = sys.argv[1]

    #headers used to put the api key, requirement by the api
    headers={
          "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
	        "X-RapidAPI-Key": api_key,#"7e29a5c4d5msh7de8b81c579766fp1ed591jsn8bdf0c862b13",
          "Content-Type": "application/json"
        }

    #list of stocks
    stocks = [ "FB", "AMZN", "GOOGL", "NFLX"]

    data_folder = "./data/"


    #for loop to include each stock one by one
    for stock in stocks:
        url = host_url + end_point_historic + common_parameter + "&symbol=" + stock

        print("Executing GET api for yahoo finance for stock: " + stock)

        #get request to retrieve data from the api
        response = requests.get(url, headers=headers)
        #creating file name
        filename = stock + ".json"

        print("Creating file: " + filename)
        with open(data_folder + filename, 'w') as fp:
           json.dump(response.json(), fp)
