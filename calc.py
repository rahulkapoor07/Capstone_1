import requests

def popular_ticker():
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"

    querystring = {"region":"US"}

    headers = {
        'x-rapidapi-key': "1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    final = response.json()["finance"]["result"][0]["quotes"]
    data = []
    for el in final:
        if el["quoteType"] == "EQUITY":
            element = {
                "name" : el["longName"],
                "symbol" : el["symbol"],
                "price" : el["regularMarketPrice"]
            }
            data.append(element)
    return data