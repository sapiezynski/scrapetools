import requests
import re
import json



def extract_header(header_str):
    """
    given a string in the format of '-H \''key: value\'' it returns a dictionary with
    the corresponding key and value
    
    Args:
        header_str (str): string containing a header in the curl format

    Returns:
        header_dict (dict): a dictionary representation of that header

    """

    header_parts = header_str.split('-H ')[1].replace('\'','').split(': ')
    key = header_parts[0]
    value = ': '.join(header_parts[1:])
    return {key: value}

def extract_headers(curl_str):
    """
    given a whole result of Copy as cURL it extract all the headers and 
    represents them as a dictionary

    Args:
        curl_str (str): string as copied from the browser developer tools

    Returns:
        headers_dict (dict): a dictionary of all headers
    """

    pattern = '-H \'[^\']+\''
    headers = re.findall(pattern, curl_str)
    headers_dict = {}
    for header in headers:
        headers_dict.update(extract_header(header))
    return headers_dict

def parse_url(url):
    """
    given a whole url, breaks it down to base url and a dictionary of get parameters

    Args:
        url (str): a whole url

    Returns:
        url_dict (dict): a dictionary containing the 'base_url' as well as a dictionary of 'params'
    """

    unquoted = requests.utils.unquote(url)
    url_parts = unquoted.split('?')
    base = url_parts[0]
    
    if len(url_parts) == 1:
        return {'base_url':base, 'params':{}}
    
    params = url_parts[1]
    params_dict = {}
    
    for param in params.split('&'):
        param_parts = param.split('=')
        key = param_parts[0]
        value = '='.join(param_parts[1:])
        params_dict[key] = value
        
    return {'base_url':base, 'params':params_dict}


def parse_data(curl_str):
    """
    given the whole Copy as cURL string, extracts the data passed in a POST
    (or nothing if it was a GET request)

    Args:
        curl_str (str): Copy as cURL string from the dev tools

    Returns:
        data_dict (dict): a dictionary representation of the data passed in the POST request
    
    """
    pattern = '--data-raw \'[^\']*\''
    data = re.findall(pattern, curl_str)
    if len(data) == 0:
        return ''
    data_dict = json.loads(data[0].replace('--data-raw \'', '')[:-1])
    return data_dict


def uncurl(curl_str):
    """
    given the whole Copy as cURL string, extracts the url and get params as well as headers

    Args:
        curl_str (str): Copy as cURL string from the dev tools

    Returns:
        uncurled (dict): a dictionary representation of the cURL command
    """

    url = curl_str.split(' ')[1].replace('\'','')
    uncurled = {}
    uncurled.update(parse_url(url))
    uncurled['headers'] = extract_headers(curl_str)
    if '--data-raw' in curl_str:
        uncurled['data'] = parse_data(curl_str)

    return uncurled

def request(uncurled):
    """
    given the uncurled request from the uncurl function, it makes a get request with the url and headers

    Args:
        uncurled (dict): the result of the uncurl function

    Returns:
        response (requests.Response): the result of the request
    """
    # params = '&'.join([f'{key}={value}' for key, value in uncurled['params'].items()])
    # url = f'{uncurled["base_url"]}?{params}'
    if 'data' in uncurled:
        return requests.post(uncurled['base_url'], 
            params = uncurled['params'], 
            headers = uncurled['headers'],
            data = uncurled['data'])
    else:
        return requests.get(uncurled['base_url'], 
            params = uncurled['params'], 
            headers = uncurled['headers'])

