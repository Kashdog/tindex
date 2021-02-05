import requests

url = "https://twitter.com"
proxy_host = "proxy.crawlera.com"
proxy_port = "8010"
proxy_auth = "2e824ba6de5f4ea199f59b87586845a8:" # Make sure to include ':' at the end
proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
      "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

r = requests.get(url, proxies=proxies,
                 verify=False)

print(r)