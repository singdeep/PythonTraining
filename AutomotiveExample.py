import requests

API_KEY = 'AIzaSyArB5LScK5-wlulS300EaE3t0Tx4Qw1Db4'
ZIP_CODE = '46807'
CATEGORY = 'car_repair'

url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?key={API_KEY}&query=in+{ZIP_CODE}'

try:
    response = requests.get(url)
    response.raise_for_status()
    results = response.json()['results']

    for result in results:
        name = result['name']
        address = result['formatted_address']
        phone = result['formatted_phone_number'] if 'formatted_phone_number' in result else 'N/A'
        print(f'{name}\n{address}\nPhone: {phone}\n')
except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Something went wrong:", err)

