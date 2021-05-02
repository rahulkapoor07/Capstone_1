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
    stock_data = []
    crypto_data = []
    for el in final:
        if el["quoteType"] == "EQUITY":
            element1 = {
                "name" : el["shortName"],
                "symbol" : el["symbol"],
                # "price" : el["regularMarketPrice"]
            }
            stock_data.append(element1)
        elif el["quoteType"] == "CRYPTOCURRENCY":
            element2 = {
                "name" : el["shortName"],
                "symbol" : el["symbol"],
                # "price" : el["regularMarketPrice"]
            }
            crypto_data.append(element2)
    return [stock_data, crypto_data]

# def search_stock(symbol, region):
#     url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"

#     querystring = {"symbol":symbol,"region":region}

#     headers = {
#     'x-rapidapi-key': "1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654",
#     'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)
#     quoteSource = response.json()["price"]["quoteSourceName"]
#     if quoteSource == "CoinMarketCap":
#         crypto_price = response.json()["price"]["regularMarketPrice"]["fmt"]
#         crypto_name = response.json()["price"]["shortName"]
#         return ["crypto", crypto_name, crypto_price]
#     elif quoteSource == "Nasdaq Real Time Price":
#         marketOpenPrice = response.json()["price"]["regularMarketPrice"]["fmt"]
#         stock_name = response.json()["price"]["shortName"]
#         return ["stock", stock_name, marketOpenPrice]
#     else:
#         return ["not found", "not found", "not found"]
