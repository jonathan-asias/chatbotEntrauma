from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import json

app = Flask(__name__)
app.secret_key = 'entrauma_unal_secret_key'

# Inicializar el modelo de IA
print("Cargando modelo de IA para ENtrauma...")
try:
    chatbot_pipeline = pipeline(
        "text-generation",
        model="gpt2",
        max_length=50,
        do_sample=True,
        temperature=0.8,
        pad_token_id=50256
    )
    print("✅ Modelo GPT-2 cargado correctamente")
    ai_available = True
except Exception as e:
    print(f"❌ Error cargando modelo GPT-2: {e}")
    try:
        chatbot_pipeline = pipeline(
            "text-generation",
            model="distilgpt2",
            max_length=30,
            do_sample=True,
            temperature=0.7
        )
        print("✅ Modelo DistilGPT-2 cargado correctamente")
        ai_available = True
    except Exception as e2:
        print(f"❌ Error cargando modelo DistilGPT-2: {e2}")
        chatbot_pipeline = None
        ai_available = False

# Flujo completo de ENtrauma - Universidad Nacional de Colombia
questions_flow = {
    "start": {
        "question": "¿Requiere orientación relacionada con algún trauma dental o bucal?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa para orientación de trauma dental",
        "next_states": ["pregunta_2", "mensaje_final_6"]
    },
    "pregunta_2": {
        "question": "Es usted (1) un usuario, paciente, cuidador, afectado. (2) un profesional en salud.",
        "ai_prompt": "Genera 2 opciones de respuesta: una para usuario/paciente y otra para profesional en salud",
        "next_states": ["mensaje_1", "mensaje_2"]
    },
    "mensaje_1": {
        "question": "Ayúdenos a conocer su caso. Por favor responda las siguientes preguntas:",
        "ai_prompt": "Genera 2 opciones de respuesta: una para continuar y otra para cancelar",
        "next_states": ["pregunta_3", "despedida"]
    },
    "pregunta_3": {
        "question": "¿El diente se salió de la boca?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre avulsión dental",
        "next_states": ["recomendacion_1", "pregunta_4_no"]
    },
    "pregunta_4_si": {
        "question": "¿El diente se fracturó?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre fractura dental",
        "next_states": ["recomendacion_2", "pregunta_5_no"]
    },
    "pregunta_4_no": {
        "question": "¿El diente se fracturó?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre fractura dental",
        "next_states": ["recomendacion_2", "pregunta_5_no"]
    },
    "pregunta_5_si": {
        "question": "¿El diente cambió de posición?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre luxación dental",
        "next_states": ["recomendacion_3", "pregunta_6_no"]
    },
    "pregunta_5_no": {
        "question": "¿El diente cambió de posición?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre luxación dental",
        "next_states": ["recomendacion_3", "pregunta_6_no"]
    },
    "pregunta_6_si": {
        "question": "¿Tiene una lesión en mentón, labios, lengua y/o encía?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre lesiones de tejidos blandos",
        "next_states": ["recomendacion_4", "pregunta_7_no"]
    },
    "pregunta_6_no": {
        "question": "¿Tiene una lesión en mentón, labios, lengua y/o encía?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre lesiones de tejidos blandos",
        "next_states": ["recomendacion_4", "pregunta_7_no"]
    },
    "pregunta_7_si": {
        "question": "¿Usted presenta dolor en este momento?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre dolor actual",
        "next_states": ["mensaje_final_1", "mensaje_final_1"]
    },
    "pregunta_7_no": {
        "question": "¿Usted presenta dolor en este momento?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre dolor actual",
        "next_states": ["mensaje_final_1", "mensaje_final_1"]
    },
    "mensaje_2": {
        "question": "Ayúdenos a conocer su caso. Por favor responda las siguientes preguntas:",
        "ai_prompt": "Genera 2 opciones de respuesta: una para continuar y otra para cancelar",
        "next_states": ["pregunta_8", "despedida"]
    },
    "pregunta_8": {
        "question": "¿Está con su paciente en este momento y requiere una orientación oportuna o una asesoría programada?",
        "ai_prompt": "Genera 3 opciones de respuesta: orientación oportuna, asesoría programada, ninguna de las anteriores",
        "next_states": ["mensaje_final_2", "mensaje_final_3", "pregunta_9"]
    },
    "pregunta_9": {
        "question": "¿Le interesa adquirir un Kit de atención inicial para trauma dentoalveolar?",
        "ai_prompt": "Genera 2 opciones de respuesta: una afirmativa y una negativa sobre interés en kit de trauma",
        "next_states": ["mensaje_final_4", "mensaje_final_5"]
    },
    "recomendacion_1": {
        "question": "recomendacion_1",
        "ai_prompt": "Sin opciones - solo mostrar recomendación",
        "next_states": ["pregunta_4_si"]
    },
    "recomendacion_2": {
        "question": "recomendacion_2", 
        "ai_prompt": "Sin opciones - solo mostrar recomendación",
        "next_states": ["pregunta_5_si"]
    },
    "recomendacion_3": {
        "question": "recomendacion_3",
        "ai_prompt": "Sin opciones - solo mostrar recomendación", 
        "next_states": ["pregunta_6_si"]
    },
    "recomendacion_4": {
        "question": "recomendacion_4",
        "ai_prompt": "Sin opciones - solo mostrar recomendación",
        "next_states": ["pregunta_7_si"]
    }
}

# Mensajes finales y de bienvenida
messages = {
    "bienvenida": "Bienvenido. Este es el servicio ENtrauma de la Facultad de Odontología de la Universidad Nacional de Colombia. Gracias por confiar en nosotros.",
    "mensaje_final_1": "Diligencie el siguiente formulario y agende su cita virtual. En breve, un experto lo atenderá. Enlace: https://www.entrauma.vortico.co/registrar-mis-datos",
    "mensaje_final_2": "Haga clic en el siguiente formulario para iniciar el proceso, por favor compártenos tus datos. Recuerde que las citas tienen un valor de $25.000. En breve, un asistente lo atenderá. Enlace: https://www.entrauma.vortico.co/registrar-mis-datos",
    "mensaje_final_3": "Este servicio nos dará la oportunidad de darle una orientación programada con un especialista. Haga clic en el siguiente formulario y seleccione día y hora de la orientación virtual. Recuerde que las citas tienen un valor de $20.000. Enlace: https://www.entrauma.vortico.co/registrar-mis-datos",
    "mensaje_final_4": "Haga clic en el siguiente enlace: Kit de atención inicial para trauma dentoalveolar. Gracias por contactarnos, si tiene alguna inquietud adicional escribanos al correo: entraumafo_bog@unal.edu.co",
    "mensaje_final_5": "Gracias por contactarnos, si tiene alguna inquietud adicional escribanos al correo: entraumafo_bog@unal.edu.co",
    "mensaje_final_6": "Si requiere atención odontológica general o especializada, comuníquese con el servicio de atención al usuario: atusuario_fobog@unal.edu.co",
    "despedida": "Gracias por usar el servicio ENtrauma. ¡Que tenga un excelente día!"
}

# Recomendaciones para respuestas afirmativas
recommendations = {
    "recomendacion_1": "🚨 RECOMENDACIÓN URGENTE 🚨\n\nPor favor recupérelo y siga las siguientes instrucciones para conservarlo: NO lo manipule, No lo lave, No lo limpie. Introdúzcalo en un recipiente limpio en leche o sales de hidratación oral. Es prioritario que agende su cita de teleorientación de manera inmediata. Lo invitamos a iniciar el proceso para acceder a la teleorientación.\n\n🔗 https://www.entrauma.vortico.co/registrar-mis-datos",
    
    "recomendacion_2": "🚨 RECOMENDACIÓN URGENTE 🚨\n\nPor favor recupérelo y siga las siguientes instrucciones para conservarlo: NO lo manipule, No lo lave, No lo limpie. Introdúzcalo en un recipiente limpio en leche o sales de hidratación oral. Es prioritario que agende su cita de teleorientación de manera inmediata. Lo invitamos a iniciar el proceso para acceder a la teleorientación.\n\n🔗 https://www.entrauma.vortico.co/registrar-mis-datos",
    
    "recomendacion_3": "🚨 RECOMENDACIÓN URGENTE 🚨\n\nPor favor trate de regresarlo a su posición original. Es prioritario que agende su cita de teleorientación en ENtrauma, por favor, inicie el proceso y acceda a la orientación.\n\n🔗 https://www.entrauma.vortico.co/registrar-mis-datos",
    
    "recomendacion_4": "🚨 RECOMENDACIÓN URGENTE 🚨\n\nLave cuidadosamente la superficie. Es prioritario que agende su cita de teleorientación en ENtrauma, por favor, inicie el proceso y acceda a la orientación.\n\n🔗 https://www.entrauma.vortico.co/registrar-mis-datos"
}

class ENtraumaBot:
    def __init__(self):
        self.current_state = "bienvenida"
        self.questions_flow = questions_flow
        self.messages = messages
        self.recommendations = recommendations
        self.generated_answers = {}
        self.conversation_history = []
        self.user_type = None  # 'usuario' o 'profesional'
    
    def get_current_question(self):
        if self.current_state in self.messages:
            return self.messages[self.current_state]
        elif self.current_state in self.recommendations:
            return self.recommendations[self.current_state]
        elif self.current_state in self.questions_flow:
            return self.questions_flow[self.current_state]["question"]
        else:
            return "Estado no encontrado"
    
    def generate_ai_answers(self):
        """Genera opciones de respuesta usando IA"""
        if self.current_state in self.messages:
            return {"Continuar": "next"}
        elif self.current_state in self.recommendations:
            return {"Continuar": "next"}
        
        if not ai_available or not chatbot_pipeline:
            return self.get_fallback_answers()
        
        state = self.questions_flow[self.current_state]
        
        # Si ya generamos respuestas para este estado, las devolvemos
        if self.current_state in self.generated_answers:
            return self.generated_answers[self.current_state]
        
        try:
            # Generar opciones basadas en el prompt
            options = self.generate_smart_options(state['ai_prompt'])
            
            # Mapear opciones a estados
            answers = {}
            next_states = state["next_states"]
            for i, option in enumerate(options):
                if i < len(next_states):
                    answers[option] = next_states[i]
            
            # Guardar en cache
            self.generated_answers[self.current_state] = answers
            
            return answers
            
        except Exception as e:
            print(f"Error generando respuestas IA: {e}")
            return self.get_fallback_answers()
    
    def generate_smart_options(self, prompt):
        """Genera opciones inteligentes basadas en el prompt"""
        prompt_lower = prompt.lower()
        
        if "afirmativa y una negativa" in prompt_lower:
            if "orientación de trauma dental" in prompt_lower:
                return ["Sí, requiero orientación", "No, no requiero orientación"]
            elif "usuario/paciente" in prompt_lower:
                return ["Soy usuario/paciente/cuidador", "Soy profesional en salud"]
            elif "avulsión dental" in prompt_lower:
                return ["Sí, el diente se salió", "No, el diente no se salió"]
            elif "fractura dental" in prompt_lower:
                return ["Sí, el diente se fracturó", "No, el diente no se fracturó"]
            elif "luxación dental" in prompt_lower:
                return ["Sí, el diente cambió de posición", "No, el diente no cambió de posición"]
            elif "lesiones de tejidos blandos" in prompt_lower:
                return ["Sí, tengo lesión en tejidos blandos", "No, no tengo lesión en tejidos blandos"]
            elif "dolor actual" in prompt_lower:
                return ["Sí, tengo dolor", "No, no tengo dolor"]
            elif "interés en kit" in prompt_lower:
                return ["Sí, me interesa el kit", "No, no me interesa el kit"]
            else:
                return ["Sí", "No"]
        
        elif "3 opciones" in prompt_lower:
            return ["Solicitar orientación oportuna", "Solicitar asesoría programada", "Ninguna de las anteriores"]
        
        elif "continuar y otra para cancelar" in prompt_lower:
            return ["Continuar", "Cancelar"]
        
        else:
            return ["Opción 1", "Opción 2"]
    
    def get_fallback_answers(self):
        """Respuestas de respaldo si la IA falla"""
        if self.current_state in self.messages:
            return {"Continuar": "next"}
        
        return self.generate_smart_options(self.questions_flow[self.current_state]["ai_prompt"])
    
    def process_answer(self, answer):
        answers = self.generate_ai_answers()
        
        if answer in answers:
            # Guardar historial
            self.conversation_history.append({
                'question': self.get_current_question(),
                'answer': answer,
                'state': self.current_state
            })
            
            # Determinar el siguiente estado
            next_state = answers[answer]
            
            # Lógica especial para flujos
            if self.current_state == "pregunta_2":
                if "usuario" in answer.lower() or "paciente" in answer.lower():
                    self.user_type = "usuario"
                else:
                    self.user_type = "profesional"
            
            # Manejar estados especiales
            if next_state == "next":
                if self.current_state == "bienvenida":
                    self.current_state = "start"
                elif self.current_state == "mensaje_1":
                    self.current_state = "pregunta_3"
                elif self.current_state == "mensaje_2":
                    self.current_state = "pregunta_8"
                elif self.current_state == "recomendacion_1":
                    self.current_state = "pregunta_4_si"
                elif self.current_state == "recomendacion_2":
                    self.current_state = "pregunta_5_si"
                elif self.current_state == "recomendacion_3":
                    self.current_state = "pregunta_6_si"
                elif self.current_state == "recomendacion_4":
                    self.current_state = "pregunta_7_si"
                else:
                    self.current_state = "despedida"
            else:
                self.current_state = next_state
            
            return True
        return False
    
    def is_end_state(self):
        return self.current_state in ["mensaje_final_1", "mensaje_final_2", "mensaje_final_3", 
                                    "mensaje_final_4", "mensaje_final_5", "mensaje_final_6", "despedida"]
    
    def reset(self):
        self.current_state = "bienvenida"
        self.generated_answers = {}
        self.conversation_history = []
        self.user_type = None
    
    def get_summary(self):
        """Genera un resumen de la conversación"""
        if not self.conversation_history:
            return "No hay historial de conversación."
        
        summary = "Resumen de la consulta ENtrauma:\n"
        for entry in self.conversation_history:
            summary += f"- {entry['answer']}\n"
        
        return summary

# Inicializar el bot
bot = ENtraumaBot()

@app.route('/')
def index():
    return render_template('entrauma.html')

@app.route('/start', methods=['POST'])
def start_conversation():
    bot.reset()
    return jsonify({
        'question': bot.get_current_question(),
        'answers': bot.generate_ai_answers(),
        'is_end': bot.is_end_state(),
        'ai_available': ai_available
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    answer = data.get('answer', '')
    
    if bot.process_answer(answer):
        if bot.is_end_state():
            summary = bot.get_summary()
            return jsonify({
                'question': bot.get_current_question(),
                'answers': {},
                'is_end': True,
                'summary': summary
            })
        else:
            return jsonify({
                'question': bot.get_current_question(),
                'answers': bot.generate_ai_answers(),
                'is_end': bot.is_end_state()
            })
    else:
        return jsonify({
            'error': 'Respuesta no válida. Por favor, selecciona una de las opciones disponibles.',
            'question': bot.get_current_question(),
            'answers': bot.generate_ai_answers(),
            'is_end': bot.is_end_state()
        })

@app.route('/reset', methods=['POST'])
def reset_conversation():
    bot.reset()
    return jsonify({'status': 'reset'})

@app.route('/status')
def status():
    return jsonify({
        'ai_available': ai_available,
        'model_loaded': chatbot_pipeline is not None,
        'current_state': bot.current_state,
        'user_type': bot.user_type
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor ENtrauma - Universidad Nacional de Colombia...")
    print(f"🤖 IA disponible: {ai_available}")
    print("📱 Accede a: http://localhost:5003")
    app.run(debug=True, host='0.0.0.0', port=5003)
