# %%
url = "http://localhost:5000/api/payment-status"
data_payment_status = {
    "customerID": "12345",
    "Nome": "Maria Silva",
    "PaymentMethod": "Cartão de Crédito",
    "CardExpiryDate": "2025-12-31",
    "LastPaymentDate": "2024-09-01",
    "SubscriptionStatus": "Ativa",
    "FraudSuspected": "Não"
}

response = requests.post(url, json=data_payment_status)
print(response.json())

# %%
import requests

url = "http://localhost:5000/api/offer"
data_offer = {
    "customerID": "12345",
    "Nome": "Maria Silva",
    "Idade": 30,
    "RendaReais": 4500,
    "Partner": "Sim",
    "Dependents": 2,
    "PhoneService": "Sim",
    "InternetService": "Fibra",
    "MonthlyCharges": 150,
    "DeviceProtection": "Sim",
    "StreamingTV": "Sim",
    "StreamingMovies": "Sim",
    "Contract": "Anual",
    "PaymentMethod": "Cartão de Crédito",
    "TotalCharges": 1800,
    "TVUsageHours": 20,
    "InternetUsageGB": 100,
    "PhoneUsageHours": 30,
    "PreviousPurchases": ["Pacote de internet", "Streaming"]
}

response = requests.post(url, json=data_offer)
print(response.json())

# %%
import requests

url = "http://localhost:5000/api/persona"

customer_data = {
    "Nome": "Maria",
    "Idade": 20,
    "SeniorCitizen": 0,
    "gender": "Feminino"
}

response = requests.post(url, json=customer_data)

if response.status_code == 200:
    result = response.json()
    print("Persona identificada:", result["persona"])
else:
    print("Erro:", response.status_code, response.text)

# %%
import requests

url = 'http://localhost:5000/api/chat'

data = {
    "user_input": "Como posso efetuar um pagamento?",
    "customer_data": {
        "Nome": "Maria",
        "Idade": 70,
        "SeniorCitizen": 1,
        "gender": "Feminino"
    }
}

try:
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        print("Resposta do assistente:", response_data['response'])
    else:
        print(f"Erro ao chamar a API: {response.status_code}, {response.text}")
except requests.RequestException as e:
    print(f"Ocorreu um erro durante a requisição: {e}")

# %%
