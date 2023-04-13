import requests

CLOUD_API_KEY = 'AIzaSyArB5LScK5-wlulS300EaE3t0Tx4Qw1Db4'
address = '46807'
radius = 50000  # radius in meters, adjust as needed
type_ = 'restaurant'

#url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={CLOUD_API_KEY}&location=37.7749,-122.4194&radius=1000&type=restaurant'
url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={CLOUD_API_KEY}&location=37.7749,-122.4194&radius=10000&type=restaurant&fields=name,rating,place_id'

response = requests.get(url)
print(response.json())
results = response.json()['results']

for result in results:
    name = result['name']
    address = result['vicinity']
    placeId = result['place_id']
    #phone = result['formatted_phone_number']
    rating = result['rating'] if 'rating' in result else 'N/A'
    print(f'{name}\n{address}\n{placeId}\n + Rating: {rating}\n')

