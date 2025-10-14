import requests

def ask_mistral(prompt, max_length=200):
    """Envoie une requête au LLM sur le serveur"""
    url = "http://localhost:8000/generate"
    
    response = requests.post(url, json={
        'prompt': prompt,
        'max_length': max_length
    })
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Erreur: {response.status_code}"

# Test
if __name__ == "__main__":
    print("Test de connexion au serveur...")
    health = requests.get("http://localhost:8000/health")
    print("Statut:", health.json())
    
    print("\nEnvoi d'une question au LLM...")
    reponse = ask_mistral("Bonjour, peux-tu te présenter en une phrase ?", max_length=1000)
    print("\nRéponse du LLM:")
    print(reponse)