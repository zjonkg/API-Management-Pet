from google import genai

client = genai.Client(api_key="AIzaSyAJVr-hI02-yzG3Utj8yaZTAVDMRJlTFKA")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)