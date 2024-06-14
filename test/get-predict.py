import requests

# Contoh lokasi, Jakarta
LATITUDE = -6.2088
LONGITUDE = 106.8456

# Radius untuk mencari tempat lokasi, dalam meter
RADIUS = 2000

# Jenis tempat yang ingin dicari (contoh: kebun binatang, pusat kebudayaan)
# Kategori mengacu pada Table A Places API
INCLUDED_TYPES = ["restaurant", "cultural_center"]
INCLUDED_TYPES_PARAMS = "&".join([f"includedTypes={type}" for type in INCLUDED_TYPES])

# Limit output prediksi
LIMIT = 3


def filter_response(response):
    for i, place in enumerate(response):
        print(f"Peringkat {i+1}: {place['displayName']['text']}")
        print(f"Address: {place['formattedAddress']}")
        print(f"Location: {place['location']}")
        print(f"Average sentiment: {place['averageSentiment']}")
        print("---------------------------------")


def main():
    url_get_data = f"http://127.0.0.1:8000/api/get-travel-spots?{INCLUDED_TYPES_PARAMS}&radius={RADIUS}&longitude={LONGITUDE}&latitude={LATITUDE}"
    url_post_data = f"http://127.0.0.1:8000/api/predict?limit={LIMIT}"

    response = requests.get(url_get_data).json()
    predict_response = requests.post(url_post_data, json=response)

    print(predict_response.json())

    print("Filtered Response:")
    filter_response(predict_response.json())


main()