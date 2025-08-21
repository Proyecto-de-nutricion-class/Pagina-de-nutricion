from flask import Flask, request, jsonify
from langchain_community.llms import LlamaCpp
from flask_cors import CORS
from pathlib import Path
from langchain.prompts import PromptTemplate

app = Flask(__name__)
CORS(app) 

def cargar_modelo():
    model_path = r"C:\Users\josel\Downloads\gemma-2-2b-it-IQ3_M.gguf"

    # Configuración del modelo
    model_config = {
        "n_ctx": 4096,
        "temperature": 0.6,
        "max_tokens": 512,
        # "stop": ["\n", "Usuario:", "IA:"],
    }
    
    model = LlamaCpp(model_path=str(model_path), **model_config)
    return model

def obtener_respuesta(model, prompt_str):
    try:
        response = model(prompt_str)
        return response
    except Exception as e:
        return f"Error al ejecutar el modelo: {e}"
    
model = cargar_modelo()
@app.route('/api/chat', methods=['POST'])
def handle_chat():
    data = request.json
    user_message = data.get('message', '')

    prompt_template = PromptTemplate.from_template(
        "Instrucciones: Eres un asistente útil y respondes en español.\n"
        "Pregunta del usuario: {user_input}\n"
        "Respuesta:"
    )
    
    prompt_str = prompt_template.format(user_input=user_message)
    
    print("\n--- Prompt enviado al modelo ---")
    print(prompt_str)
    print("---------------------------------\n")
    
    respuesta = obtener_respuesta(model, prompt_str)
    
    print("\n--- Respuesta del modelo (modo prueba) ---")
    print(respuesta)
    print("------------------------------------------\n")

    respuesta_limpia = respuesta.strip().replace("Bot: ", "")
    return jsonify({"respuesta": respuesta_limpia})

if __name__ == "__main__":
    app.run(port=5000)
   # app = Flask(__name__)
# if _name_ == "_main_":
#     while True:
#         user_input = input("Ingresa tu pregunta (o 'salir' para terminar): ")
#         if user_input.lower() == 'salir':
#             break
        
#         prompt = ChatPromptTemplate.from_template("Responde a la siguiente pregunta: {user_input}")
#         prompt_str = prompt.format_prompt(user_input=user_input).to_string()
        
#         respuesta = obtener_respuesta(model, prompt_str)
#         print("Respuesta del modelo:")
#         print(respuesta)