import requests
API_KEY = "8150684f563b54958fe32d30087469a0"
city = input("Enter city name: ")
url = "http://api.openweathermap.org/data/2.5/weather"
parameters = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}
response = requests.get(url, params=parameters)
print(response.status_code)
print(response.json())