#!/bin/bash

# Make GET request and save response to data3.json
curl -sL "http://127.0.0.1:8000/api/get-travel-spots?includedTypes=restaurant&includedTypes=cultural_center&radius=2000&longitude=106.8456&latitude=-6.2088" -o data3.json

# Check if GET request was successful
if [ $? -eq 0 ]; then
	echo "Raw GET Response:"
	cat data3.json
	echo
	# Make POST request with data3.json and print the response
	echo "Raw POST Response:"
	curl -sL -X POST -H "Content-Type: application/json" -d @data3.json "http://127.0.0.1:8000/api/predict?limit=3"
else
	echo "GET request failed"
fi
