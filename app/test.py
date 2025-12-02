from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain AI in a few words"
)
print(response.text)