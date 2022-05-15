from bs4 import BeautifulSoup
import requests

def get_template_list():
    response = requests.request("GET", f"http://apimeme.com/?page=1")
    ob = BeautifulSoup(response.text, "html.parser")
    return [option["value"] for option in ob.find_all("option")]