import urllib.parse
import re
import boto3
import json
from urllib.parse import unquote

amazon_base_url = "https://www.amazon.com/"

# dynamodb = boto3.client('dynamodb', region_name='us-east-1')
# TABLE_NAME = "scrappers-affilaite"

# response = dynamodb.get_item(
#     TableName=TABLE_NAME,
#     Key={
#         'id': {'N':'1'},
#     }
# )

def strip_text_from_price(text):
    price = re.search('[0-9.]+', text)
    if price is not None and price.group() is not None:
        return price.group()
    print("strip_text_from_price regex failed")
    return text


def getAffiliates():
    if response["Item"] is not None:
        print("getAffiliates")
        return json.loads(response['Item']["affiliates"]["S"])
    return None


def format_impact_affiliate_link(baseUrl, link, which):
    print("helpers starts===>")
    apiUserAffiliate = getAffiliates()
    print("apiUserAffiliate-->",apiUserAffiliate)
    #If APIkey not found return regular link
    if apiUserAffiliate is None:
        return link
    print("ssssssssssss")
    apiUserAffiliate = apiUserAffiliate[which]
    print("eeeeeeeeeeee")
    newLink = baseUrl
    if "apiKey1" in apiUserAffiliate:
        newLink += apiUserAffiliate["apiKey1"]
    else:
        print("NO APIKEY ONE") 
    if "apiKey2" in apiUserAffiliate:
        newLink += "/" + apiUserAffiliate["apiKey2"]
    if "apiKey3" in apiUserAffiliate:
        newLink += "/" + apiUserAffiliate["apiKey3"]
    newLink += "?u=" + urllib.parse.quote_plus(link)
    print("helpers end===>", newLink)
    return newLink


def format_amazon_affiliate_link(link):
    apiUserAffiliate = getAffiliates()["amazon"]

    if "apiKey" in apiUserAffiliate:
        apiUserApiKey = apiUserAffiliate["apiKey"]
    else: 
        print("NO API KEY")

    link = unquote(link)
    find = re.search("dp\/\w*\/", link)
    item = ""
    if find is not None and find.group(0) is not None:
        item = find.group(0)
        newLink = amazon_base_url + item + "?tag=" + apiUserApiKey
        return newLink
    return link

# url="/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A01522512Q5EXOI6OB5Q2&url=%2FHP-Quad-Core-i5-1035G1-Bluetooth-Accessories%2Fdp%2FB08B1F6YQ8%2Fref%3Dsr_1_1_sspa%3Fdchild%3D1%26keywords%3Dlaptop%26qid%3D1599491642%26sr%3D8-1-spons%26psc%3D1&qualifier=1599491642&id=5496492327270595&widgetName=sp_atf"
# link = unquote(url)
# print(amazon_affiliate(link))
 