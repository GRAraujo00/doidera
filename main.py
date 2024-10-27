from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# Habilitar CORS para permitir acesso via navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Configurar a API do Gemini
API_KEY = "AIzaSyCVkItx4781WnhJWFkIk6YFelhxMTLVWpk"
genai.configure(api_key=API_KEY)

# Lista de tipos de bolo possíveis
tipos_de_bolo = [
    "chocolate", "cenoura", "milho", "fubá", "laranja", "limao", "maracujá", "coco", 
    "baunilha", "morango", "abacaxi", "banana", "maçã", "canela", "nozes", "castanha", 
    "pistache", "amêndoas", "queijo", "creme", "brigadeiro", "cobertura de chocolate",
    "frutas vermelhas", "doce de leite", "marmore", "aipim", "mandioca", "pé de moleque", 
    "fofo", "pão de ló", "formigueiro", "jilo", "jiló"
]

@app.get("/receitas/{query}")
async def get_receita(query: str):
    # Verifica se a consulta contém a palavra "bolo"
    if "bolo" not in query.lower():
        raise HTTPException(status_code=400, detail="Somente receitas de bolo são aceitas.")
    
    # Extrai o tipo de bolo da consulta
    tipo_bolo = query.lower().replace("bolo de ", "").strip()
    
    # Verifica se o tipo de bolo está na lista de tipos de bolo
    if tipo_bolo not in tipos_de_bolo:
        raise HTTPException(status_code=400, detail=f"O tipo de bolo '{tipo_bolo}' não é reconhecido. Tente um dos seguintes: {', '.join(tipos_de_bolo)}.")
    
    try:
        # Utilizando o modelo do Gemini para gerar conteúdo
        response = genai.generate_content(f"receita de {query}")
        
        # Garante que o conteúdo seja retornado integralmente
        receita_completa = response.text if response.text else "A receita não foi encontrada ou está mal formatada."
        
        return {
            "ingredientes": receita_completa,
            "instrucoes": ""  # Deixa instruções em branco para evitar conflito
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a solicitação.")
