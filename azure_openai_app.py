import openai

openai.api_key = "AZURE_OPENAI_KEY"
openai.api_base = "https://RESOURCE_NAME.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = "2023-05-15"

response = openai.ChatCompletion.create(
    engine="gpt-35-turbo",
    messages=[{"role": "user", "content": "Tell me a joke"}]
)

print(response.choices[0].message["content"])
