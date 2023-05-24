HOW TO REQUEST DATA:

1/ Save the file weather.py in the same folder with your project file
2/ URL to call api: 'http://localhost:5000/api'
3/ Parameters: 
{'location' : your_function_input}

Note: your_function_input can be either:
- city (required), state (optional - US only), country (required if state provided) or 
- zipcode (US only).
For example, input can be:
"London"
"London, GB"
"Seattle"
"London, OH, US"
"98180"

Example of api call:

http://localhost:5000/api?location=Seattle

or

http://localhost:5000/api?location=98170

Data can be received in json format.

UML of weather-api:

![image](https://github.com/hsnguyen318/CS-361/assets/102455799/73fe0015-cc5d-4a6f-9a41-7d443ea6392f)
