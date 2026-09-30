import requests
from urllib.parse import quote
prompt="A violent golden retriver smoing cigar in a butcher shop"
encoded_prompt=quote(prompt)
url=(
    f"https://image.pollinations.ai/prompt/"
    f"{encoded_prompt}"
    f"?model=flux"
)
print("Generating image....")
response=requests.get(url,timeout=180)
print("Status:",response.status_code)
if response.status_code==200:
    with open("test_image.jpg","wb") as file:
        file.write(response.content)
    print("Image generated successfully")
    print("Saved as test_image.jpg")
else:
    print("Image generation failed")
    print(response.text)