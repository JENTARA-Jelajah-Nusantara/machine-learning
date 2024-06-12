import requests

url_get = "http://127.0.0.1:8000/get-travel-spots"
url = "http://127.0.0.1:8000/predict"

data = requests.get(url_get).json()

# data = {
#     "places": [
#         {
#             "name": "Monas",
#             "image": "gambar-monas.jpg",
#             "location": "Jakarta, Indonesia",
#             "description": "Tempat wisata ikonik di Jakarta",
#             "user_review": [
#                 {
#                     "text": "Tempatnya sangat bagus, sejuk, suasananya indah"
#                 },
#                 {
#                     "text": "Tempatnya sangat buruk, bangunan rusak, saya tidak rekomendasikan"
#                 }
#             ]
#         },
#         {
#             "name": "Ancol",
#             "image": "gambar-ancol.png",
#             "location": "Jakarta, Indonesia",
#             "description": "Tempat wisata air ikonik di Jakarta",
#             "user_review": [
#                 {
#                     "text": "Tempatnya biasa saja, tidak terlalu bagus, tidak terlalu buruk"
#                 },
#                 {
#                     "text": "Tempatnya sangat kotor, tidak terawat, tidak nyaman"
#                 }
#             ]
#         }
#     ]
# }

response = requests.post(url, json=data)

print(response.json())