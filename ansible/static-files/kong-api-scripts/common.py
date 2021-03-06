import urllib2, json

# Due to issue https://github.com/Mashape/kong/issues/1912
# We can't loop through all apis page by page
# Hence this work around which fetches apis with page size limited to max_page_size
# max_page_size ensures we don't bring down DB by fetching lot of rows
# If we reach a state we have more apis than max_page_size,
# Increase value of max_page_size judiciously
def get_apis(kong_admin_api_url):
    max_page_size = 1000
    apis_url_with_size_limit = "{}/apis?size={}".format(kong_admin_api_url, max_page_size)
    apis_response = json.loads(urllib2.urlopen(apis_url_with_size_limit).read())
    total_apis = apis_response["total"]
    if(total_apis > max_page_size):
        raise Exception("There are {} apis existing in system which is more than max_page_size={}. Please increase max_page_size in ansible/kong_apis.py if this is expected".format(total_apis, max_page_size))
    else:
       return apis_response["data"]

def json_request(method, url, data=None):
    request_body = json.dumps(data) if data is not None else None
    request = urllib2.Request(url, request_body)
    if data:
        request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: method
    response = urllib2.urlopen(request)
    return response
