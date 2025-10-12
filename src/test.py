#pip install openai
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

resp = client.chat.completions.create(
    model="mistral",  # ou "mistral:instruct" selon ton tag
    messages=[
        {"role":"system","content":"Tu réponds toujours en français, clairement et brièvement."},
        {"role":"user","content":"Explique l’algorithme A* en 5 points."}
    ],
    temperature=0.7,
    max_tokens=300,
)
print(resp.choices[0].message.content)
