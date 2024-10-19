# %%
import requests

url = "https://deploy-api-hacka.onrender.com/api/payment-status"
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

url = "https://deploy-api-hacka.onrender.com/api/offer"
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

url = "https://deploy-api-hacka.onrender.com/api/persona"

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

url = 'https://deploy-api-hacka.onrender.com/api/chat'
headers = {"Content-Type": "application/json"}

customer_data = {
    "Nome": "João",
    "Idade": 65,
    "SeniorCitizen": 1,
    "gender": "Male"
}

data = {
    "user_input": "Olá",
    "customer_data": customer_data
}

response = requests.post(url, json=data, headers=headers)
print(response.json())

second_input = {
    "user_input": "Quais são minhas opções de serviço?",
    "customer_data": customer_data
}

response = requests.post(url, json=second_input, headers=headers)
print(response.json())

third_input = {
    "user_input": "Quero saber mais sobre a opção 2. Consultoria Especializada",
    "customer_data": customer_data
}

response = requests.post(url, json=third_input, headers=headers)
print(response.json())
