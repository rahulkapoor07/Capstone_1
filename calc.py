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
                "price" : el["regularMarketPrice"],
                "region": el["region"]
            }
            stock_data.append(element1)
        elif el["quoteType"] == "CRYPTOCURRENCY":
            element2 = {
                "name" : el["shortName"],
                "symbol" : el["symbol"],
                "price" : el["regularMarketPrice"],
                "region": el["region"]
            }
            crypto_data.append(element2)
    return [stock_data, crypto_data]

def search_stock(symbol, region):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"

    querystring = {"symbol":symbol,"region":region}

    headers = {
    'x-rapidapi-key': "1485ec3af1msh7c54fae5d48e5cap1ef8c9jsn9f5c4864e654",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    titles = response.json()["secFilings"]["filings"]#["title"]
    urls = response.json()["secFilings"]["filings"]#[""edgarUrl""]
    summary = response.json()["assetProfile"]["longBusinessSummary"]
    officers_details = response.json()["assetProfile"]["companyOfficers"]#["name"]["title"]
    address_website = response.json()["assetProfile"]["website"]
    address_zip = response.json()["assetProfile"]["zip"]
    address_address = response.json()["assetProfile"]["address1"]
    address_city = response.json()["assetProfile"]["city"]
    address_phone = response.json()["assetProfile"]["phone"]
    address_state = response.json()["assetProfile"]["state"]
    address_country = response.json()["assetProfile"]["country"]
    address_industry = response.json()["assetProfile"]["industry"]

    address = {"address": address_address, "city" : address_city, "state": address_state,
        "zip" : address_zip, "country" : address_country, "industry" : address_industry,
        "website": address_website, "phone": address_phone}
    
    company_details = {"titles": titles, "urls": urls}

    if response.text != '':
        quoteSource = response.json()["price"]["quoteType"]
        if quoteSource == "CRYPTOCURRENCY":
            crypto_price = response.json()["price"]["regularMarketPrice"]["raw"]
            crypto_name = response.json()["price"]["shortName"]
            return {"type" : "crypto", "name" : crypto_name, "symbol" : symbol, "region" : region, "price" : crypto_price,
            "address": address, "officers": officers_details, "company_details":company_details, "summary": summary}
        elif quoteSource == "EQUITY":
            marketOpenPrice = response.json()["price"]["regularMarketPrice"]["raw"]
            stock_name = response.json()["price"]["shortName"]
            return {"type" : "stock", "name" : stock_name, "symbol" : symbol, "region" : region, "price" : marketOpenPrice,
            "address": address, "officers": officers_details, "company_details":company_details, "summary": summary}
        else:
            return ["not found", "not found", "not found"]
    else:
        return {"type" : "not found"}