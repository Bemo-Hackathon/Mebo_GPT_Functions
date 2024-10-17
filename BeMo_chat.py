# %%
import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = 'API_KEY'
BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo-0125"


def load_faq(file_path):
    try:
        faq_df = pd.read_csv(file_path, encoding='utf-8')

        if 'pergunta' not in faq_df.columns or 'resposta' not in faq_df.columns:
            raise ValueError("O arquivo deve conter as colunas 'pergunta' e 'resposta'.")

        faq_dict = dict(zip(faq_df['pergunta'].str.lower(), faq_df['resposta']))
        return faq_dict

    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
    except pd.errors.EmptyDataError:
        print("O arquivo CSV está vazio.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo FAQ: {e}")
    return {}


def load_customer_data(file_path):
    try:
        customer_df = pd.read_csv(file_path, encoding='utf-8')
        return customer_df
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
    except pd.errors.EmptyDataError:
        print("O arquivo CSV está vazio.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo de clientes: {e}")
    return pd.DataFrame()


def identify_persona(customer):
    age = customer['Idade']
    senior_citizen = customer['SeniorCitizen']
    name = customer['Nome']
    gender = customer['gender']
    
    prompt = f"""
    Com base nas seguintes informações do cliente, identifique a persona:

    Nome: {name}
    Idade: {age}
    SeniorCitizen: {senior_citizen}
    Gênero: {gender}
    
    As personas são:
    - Persona Dona Maria: Uma mulher de 70 anos com dificuldade para enxergar o aplicativo, precisa de uma comunicação clara e amigável.
    - Persona Nicolas: Um jovem de 20 anos que gosta de explorar todas as funções do aplicativo, prefere uma comunicação casual e dinâmica.
    
    Responda com uma descrição da persona (Dona Maria ou Nicolas).
    """
    
    return call_openai_api(prompt)


def greetings_persona(customer):
    persona = identify_persona(customer)

    prompt = f"""
    Baseado nas informações abaixo, gere apenas uma saudação adequada e amigável para o cliente. Não mencione a persona explicitamente.

    Nome: {customer['Nome']}
    Persona: {persona}

    Instruções:
    - Para um cliente mais velho (como Dona Maria), use uma comunicação clara, acolhedora e formal.
    - Para um cliente jovem (como Nicolas), use uma comunicação casual, amigável e dinâmica.

    Não inclua informações da persona na saudação, apenas o tom correto e a saudação amigável.

    """
    return call_openai_api(prompt)


def analyze_spending_profile(customer):
    prompt = f"""
    Analisando as seguintes informações do cliente, identifique seu perfil de compra/gasto:

    ID: {customer['customerID']}
    Nome: {customer['Nome']}
    Idade: {customer['Idade']}
    Renda: {customer['RendaReais']}
    Partner: {customer['Partner']}
    Dependents: {customer['Dependents']}
    PhoneService: {customer['PhoneService']}
    InternetService: {customer['InternetService']}
    MonthlyCharges: {customer['MonthlyCharges']}
    DeviceProtection: {customer['DeviceProtection']}
    StreamingTV: {customer['StreamingTV']}
    StreamingMovies: {customer['StreamingMovies']}
    Contract: {customer['Contract']}
    PaymentMethod: {customer['PaymentMethod']}
    TotalCharges: {customer['TotalCharges']}
    TVUsageHours: {customer['TVUsageHours']}
    InternetUsageGB: {customer['InternetUsageGB']}
    PhoneUsageHours: {customer['PhoneUsageHours']}
    PreviousPurchases: {customer['PreviousPurchases']}
    RendaReais: {customer['RendaReais']}

    Responda com uma descrição do perfil de compra/gasto do cliente.
    """

    return call_openai_api(prompt)


def suggest_offer(customer):
    spending_profile_analysis = analyze_spending_profile(customer)
    
    prompt = f"""
    Baseado nas seguintes informações, sugira a melhor oferta para o cliente:
    
    Análise do perfil de gastos: {spending_profile_analysis}

    Responda com a melhor oferta para esse cliente. Nota-se que o valor total de TotalCharges
    não deve ser alterado de maneira significante. Além disso, o valor deve ser compatível com a RendaReais do cliente.
    """

    return call_openai_api(prompt)

def notification_offer(customer):
    spending_profile_analysis = analyze_spending_profile(customer)
    
    prompt = f"""
    Baseado nas seguintes informações, gere uma notificação de oferta personalizada para o cliente:
    
    Análise do perfil de gastos: {spending_profile_analysis}
    
    Estruture a notificação da seguinte forma:
    - Título chamativo e breve que destaque a oferta. Faça uma pergunta envolvente no título.
    - Uma frase introdutória e chamativa que faça o cliente se interessar pela oferta. Evite parecer um scam.
    - Descrição clara e detalhada da oferta, explicando como ela atende ao perfil do cliente.
    - Um fechamento convidando o cliente a aproveitar a oferta.
    - Busque textos mais curtos e evite a palavra "conservador".

    Certifique-se de que o valor total de "TotalCharges" não seja alterado de maneira significante e que o valor seja compatível com a renda mensal do cliente ({customer['RendaReais']}).
    
    Responda apenas com a notificação formatada.
    """

    return call_openai_api(prompt)


def call_openai_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return "Desculpe, não consegui gerar uma resposta no momento."


def chat_with_model(model, persona, greeting, faq_dict, recommendation):
    conversation_history = [
        {"role": "system", "content": persona},
        {"role": "assistant", "content": greeting},
        {"role": "assistant", "content": f"Aqui está uma oferta recomendada para você: {recommendation}"}
    ]

    print(f"\nAssistente: {greeting}")

    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() == 'sair':
            print("Obrigado por conversar comigo. Até a próxima!")
            break

        conversation_history.append({"role": "user", "content": user_input})
        user_input_lower = user_input.strip().lower()

        if user_input_lower in faq_dict:
            response_text = faq_dict[user_input_lower]
            print(f"\nCliente: {user_input}")
            print(f"\nAssistente: {response_text}")
            conversation_history.append({"role": "assistant", "content": response_text})
            continue

        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": conversation_history
            }
            response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            assistant_response = response.json()['choices'][0]['message']['content']

            print(f"\nCliente: {user_input}")
            print(f"\nAssistente: {assistant_response}")
            
            conversation_history.append({"role": "assistant", "content": assistant_response})
        except requests.RequestException as e:
            print(f"Ocorreu um erro: {e}")

def main():
    faq_file_path = r'C:\Users\rlope\OneDrive\Área de Trabalho\HACKATHON\faq.csv'
    faq_dict = load_faq(faq_file_path)

    customer_file_path = r'C:\Users\rlope\OneDrive\Área de Trabalho\HACKATHON\customer_data.csv'
    customer_data = load_customer_data(customer_file_path)

    if not customer_data.empty:
        customer = customer_data.iloc[0]
        
        persona = identify_persona(customer)
        greeting = greetings_persona(customer)

        recommendation = suggest_offer(customer)
    else:
        persona = "Você é Be'mo, uma senhora de 70 anos. Use uma linguagem formal e clara para se comunicar."
        greeting = "Olá, eu sou Be'Mo, o Assistente Virtual da Bemobi. Como posso te ajudar hoje?"
        recommendation = "Desculpe, não consegui gerar uma oferta no momento."

    chosen_model = DEFAULT_MODEL

    chat_with_model(chosen_model, persona, greeting, faq_dict, recommendation)

if __name__ == "__main__":
    main()
