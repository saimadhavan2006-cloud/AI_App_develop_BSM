import requests

# Get all posts
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)
print(response) 

# Parse the JSON response into a list
posts = response.json()

# Print the first post and the third-to-last post
print(posts[0])
print(posts[-3])

# Make a request to a non-existent endpoint to get a 404 error
url = "https://jsonplaceholder.typicode.com/posts/999"
response = requests.get(url)
print(response)