import requests
import base64
import os
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
from read_env_var import *

def baixar_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        exit(1)

def extrair_e_salvar_imagem(html):
    soup = BeautifulSoup(html, "html.parser")

    try:
        imagem = soup.find("img")
        if not imagem or not imagem.get("src"):
            raise ValueError("Nenhuma imagem <img> com atributo src encontrada.")

        src_base64 = imagem["src"]
        if not src_base64.startswith("data:image"):
            raise ValueError("Imagem não está em formato base64.")

        header, encoded = src_base64.split(",", 1)
        img_data = base64.b64decode(encoded)

        pasta_imagens = "images"
        os.makedirs(pasta_imagens, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"imagem_{timestamp}.jpg"
        caminho_arquivo = os.path.join(pasta_imagens, nome_arquivo)

        with open(caminho_arquivo, "wb") as f:
            f.write(img_data)

        return caminho_arquivo

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        exit(1)

def codificar_imagem(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as f:
            imagem_bytes = f.read()
            return base64.b64encode(imagem_bytes).decode("utf-8")
    except Exception as e:
        print(f"Erro ao ler ou codificar a imagem: {e}")
        exit(1)

def enviar_para_inferencia(imagem_base64):
    try:
        payload = {
            "model": "microsoft-florence-2-large",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "<DETAILED_CAPTION>"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagem_base64}"
                            }
                        }
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Erro ao enviar a imagem para inferência: {e}")
        exit(1)

def submeter_resposta(resultado: dict):

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(SUBMIT_URL, json=resultado, headers=headers)
        response.raise_for_status()
        print("Resposta submetida.")
    except Exception as e:
        raise RuntimeError(f"Erro ao submeter a resposta: {e}")

def main():
    html = baixar_html(URL)
    caminho_arquivo = extrair_e_salvar_imagem(html)
    imagem_base64 = codificar_imagem(caminho_arquivo)
    resultado = enviar_para_inferencia(imagem_base64)
    print(resultado)
    submeter_resposta(resultado)

if __name__ == "__main__":
    main()