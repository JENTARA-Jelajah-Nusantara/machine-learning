# Machine Learning
## Setup
1. Install dependencies:
    - TensorFlow
    - Transformers
    - Sastrawi
    - FastAPI
    - NumPy
2. Masukkan path hasil training (format h5) ML di ```app/config.py``` ```MODEL_PATH```
3. Masukkan Google Maps API Key di ```app/routes/get_travel_spots.py``` ```"X-Goog-Api-Key": "Insert API Key di sini"```

## Jalankan API
1. Clone Repository ```git clone https://github.com/JENTARA-Jelajah-Nusantara/machine-learning.git --depth=1```
2. ```cd app```
3. Jalankan server ```fastapi dev main.py```

## Route API
Route API ada dua: ```api/get_travel_spots``` & ```/api/predict```

#### api/get_travel_spots

API ini dipakai untuk fetch data dari Google Maps API yang nantinya dipakai sebagai input model ML.

```/api/get-travel-spots?includedTypes=[KATEGORI1]&includedTypes=[KATEGORI2]&dst...&radius=[RADIUS]&longitude=[LONGITUDE]&latitude=[LATITUDE]```

Route ini dapat menerima 4 params:
1. ```includeTypes: List[str]```: Kategori tempat, contohnya zoo, restaurant, etc (berdasarkan Table A Gmaps Places API). List kategori yang cocok untuk tempat wisata masih kami susun.
2. ```Latitude: float```: Untuk mengetahui lokasi user.
3. ```Longitude: float```: untuk mengetahui lokasi user.
4. ```Radius: float```: Maksimal jarak pencarian lokasi. Misalnya 500 m, berarti tempat wisata yang direkomendasikan berada pada radius 500 m.

Contoh penggunaan.
Misalnya kita mau fetch tempat wisata dengan rincian:
1. Kategori =  zoo, restaurant.
2. Latitude = -6.2088 (Jakarta)
3. Longitude = 106.8456 (Jakarta)
4. Radius = 2000 meter

Param yang dipakai adalah:
```/api/get-travel-spots?includedTypes=zoo&includedTypes=restaurant&radius=2000&longitude=106.8456&latitude=-6.2088```

#### api/predict

```/api/predict?limit=[LIMIT]```

API ini digunakan untuk mendapat rekomendasi tempat wisata. Input API ini adalah response yang diperoleh dari ```/api/get_travel_spots```

Route ini dapat menerima 1 param:

```Limit: int```: Jumalah tempat wisata yang diinginkan user. Misalnya user pilih 3 maka API hanya return 3 rekomendasi tempat wisata.

Untuk mendapat rekomendasi tempat wisata, tinggal POST response dari ```/api/get_travel_spots``` yang berupa JSON ke API ini. Data yang diperoleh nantinya berupa list object (dengan jumlah sesuai ```Limit```) tempat wisata terbaik. List no. 1 merupakan tempat dengan hasil sentimen terbaik, dst. Ini format response yg didapat dari API ini:
```
[
   {
      "formattedAddress":"Jl. Tambak No.16A 1, Pegangsaan, Kec. Menteng, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10320, Indonesia",
      "location":{
         "latitude":-6.2060471999999995,
         "longitude":106.84860479999999
      },
      "displayName":{
         "text":"Hadramout",
         "languageCode":"id"
      },
      "reviews":[{}],
      "photos":[{}],
      "averageSentiment":4.8
   },
   dst..
]
```

Contoh penggunaan API ini bisa diliat di ```test/get_predict.py```. File ini nanti bakal output:
1. Response raw
2. Response setelah di filter