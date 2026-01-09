import os
import json
import time
import googlemaps
import csv
import math
import geocoder

# Replace 'YOUR API KEY' with your actual Google Maps API key
# View updated_with_zipcodes.csv in googleMaps/CSV for reference of output file

def initialize_gmaps(api_key):
    return googlemaps.Client(key=api_key)

def find_upscale_places(gmaps, latitude, longitude, radius=1000):
    upscale_types = ['restaurant', 'shopping_mall', 'real_estate_agency']
    upscale_keywords = ['luxury', 'upscale', 'premium']
    upscale_places = []
    location = (latitude, longitude)

    base_directory = "googleMaps/json_data"
    success_dir = os.path.join(base_directory, "success")
    error_dir = os.path.join(base_directory, "error")
    empty_dir = os.path.join(base_directory, "empty")

    for directory in [success_dir, error_dir, empty_dir]:
        os.makedirs(directory, exist_ok=True)

    for place_type in upscale_types:
        for keyword in upscale_keywords:
            try:
                time.sleep(1)
                results = gmaps.places_nearby(location=location, radius=radius, type=place_type, keyword=keyword)
                if results.get('results'):
                    save_json_data(success_dir, latitude, longitude, place_type, keyword, results)
                    upscale_places.extend(results.get('results', []))
                else:
                    save_json_data(empty_dir, latitude, longitude, place_type, keyword, results)
            except Exception as e:
                error_data = {'error': str(e)}
                save_json_data(error_dir, latitude, longitude, place_type, keyword, error_data)

    return upscale_places, len(upscale_places)

def save_json_data(directory, latitude, longitude, place_type, keyword, data):
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    subdirectory = os.path.join(directory, current_time)
    os.makedirs(subdirectory, exist_ok=True)
    filename = f"{latitude}_{longitude}_{place_type}_{keyword}.json"
    filepath = os.path.join(subdirectory, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def place_split(latitude, longitude, radius):
    new_radius = radius / 2
    lat_offset = (new_radius / 111111) * 1.414
    lng_offset = (new_radius / (111111 * math.cos(latitude * math.pi / 180))) * 1.414

    new_centers = [
        (latitude + lat_offset, longitude + lng_offset),
        (latitude + lat_offset, longitude - lng_offset),
        (latitude - lat_offset, longitude + lng_offset),
        (latitude - lat_offset, longitude - lng_offset)
    ]
    return new_centers, new_radius

def process_csv(input_csv_path, gmaps):
    results = []
    with open(input_csv_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csvreader, None)

        for index, row in enumerate(csvreader):
            county_name = row[2]
            latitude = float(row[9])
            longitude = float(row[10])
            upscale_places, score = find_upscale_places(gmaps, latitude, longitude)

            if score > 20:
                new_centers, new_radius = place_split(latitude, longitude, 1000)
                for center in new_centers:
                    lat, lng = center
                    _, new_score = find_upscale_places(gmaps, lat, lng, new_radius)
                    results.append([county_name + ' Split', lat, lng, new_score])
            else:
                results.append([county_name, latitude, longitude, score])
    return results

def main():
    api_key = 'YOUR API KEY'
    gmaps = initialize_gmaps(api_key)
    input_csv_path = 'googleMaps/CSV/correctcounties.csv'
    results = process_csv(input_csv_path, gmaps)
    output_csv_path = 'CleanedDataCSVs/googleMapsAPI_cleaned.csv'
    with open(output_csv_path, 'w', newline='') as outputfile:
        csvwriter = csv.writer(outputfile)
        csvwriter.writerow(['County', 'Latitude', 'Longitude', 'Score'])
        csvwriter.writerows(results)

if __name__ == "__main__":
    main()