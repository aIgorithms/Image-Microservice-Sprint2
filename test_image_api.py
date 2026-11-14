import requests

# The URL where our microservice is listening
url = "http://localhost:5004/image"


print("--- Testing Valid Keyword (golf) ---")

# Setup the parameters we want to send
valid_params = {
    "keyword": "golf", 
    "size": "large"
}

# Send the GET request
response_valid = requests.get(url, params=valid_params)

# Print the JSON result
print(response_valid.json())
print("\n")


print("--- Testing Missing Keyword Fallback (space) ---")

# Setup the parameters for a missing word
fallback_params = {
    "keyword": "space"
}

# Send the GET request
response_fallback = requests.get(url, params=fallback_params)

# Print the JSON result
print(response_fallback.json())