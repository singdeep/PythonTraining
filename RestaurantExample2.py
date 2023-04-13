import requests
import os

CLOUD_API_KEY = os.environ["OPENAI_API_KEY"]
location = '41.06312718035604, -85.14700344428779' #later on this could be wherever you drop the pin on the map
radius = 1000  # radius in meters, adjust as needed
type = 'restaurant'

# Define the base URL for the Nearby Search request
nearby_search_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={CLOUD_API_KEY}&location={location}&radius={radius}&type={type}&limit=3'

# Make the Nearby Search request
nearby_search_response = requests.get(nearby_search_url)
nearby_search_results = nearby_search_response.json()['results']

# Loop through the results and make a Place Details request for each place_id
for result in nearby_search_results:
    place_id = result['place_id']
    address = result['vicinity']
    place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?key={CLOUD_API_KEY}&place_id={place_id}&fields=name,rating,formatted_phone_number,website'
    place_details_response = requests.get(place_details_url)
    place_details_result = place_details_response.json()['result']

    if 'formatted_address' in place_details_result:
        address = place_details_result['formatted_address']

    name = place_details_result['name']
    phone = place_details_result.get('formatted_phone_number', 'N/A')
    rating = place_details_result.get('rating', 'N/A')
    website = place_details_result.get('website', 'N/A')

    print(f'{name}\n{address}\n{phone}\n{website}\n+ Rating: {rating}\n')