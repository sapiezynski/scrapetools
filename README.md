# scrapetools
`scrapetools` can be used to reverse engineer and modify internal API calls on webpages. 

## usage
* Start by opening the Developer Tools in your browser and indentifying which call you might want to replicate.
* Right click on that call and select "Copy -> Copy as cURL"
* paste the clipboard as a string in your notebook (with double quotation marks)
	* for example I copied a call from AllRecipes
	
	```
	curl_str = """
  curl 'https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more?search=spinach&page=2' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:86.0) Gecko/20100101 Firefox/86.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=1' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://www.allrecipes.com/search/results/?search=spinach' -H 'Cookie: removed for privacy reasons' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'TE: Trailers'
  """
	```
* transform this string into something more usable:

```
import scrapetools
uncurled = scrapetools.uncurl(curl_str)
```

* now `uncurled` is a dictionary:

```
{
  "base_url": "https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more",
  "params": {
    "search": "spinach",
    "page": "2"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=1",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.allrecipes.com/search/results/?search=spinach",
    "Cookie": "removed for privacy reasons",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers"
  }
} 
```
* we can clearly see that the search term is under `uncurled['params']['search']` and the page number is under `uncurled['params']['page']`
* we can modify either of these values and search for another ingredient or a different page:

```
uncurled['params']['page'] = 3
```
* after making the necessary adjustment, we can make the modified request:

```
response = scrapetools.request(uncurled)
```
