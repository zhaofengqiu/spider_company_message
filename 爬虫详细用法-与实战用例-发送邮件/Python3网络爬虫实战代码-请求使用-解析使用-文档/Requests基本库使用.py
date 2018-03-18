
import requests
from requests.exceptions import ReadTimeout,HTTPError,RequestException
try:
    response = requests.get('http://httpbin.org/get',timeout=0.1)
    print(response.status_code)
except ReadTimeout as e:
    print(e)
except HTTPError as e:
    print(e)
except RequestException as e:
    print(e)