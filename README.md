# 🦷 ENtrauma Chatbot

**Servicio especializado en trauma dental y bucal de la Facultad de Odontología de la Universidad Nacional de Colombia**

## 📋 Descripción

ENtrauma es un chatbot inteligente desarrollado para brindar orientación especializada en casos de trauma dental y bucal. El sistema utiliza inteligencia artificial (Transformers) para generar respuestas contextuales y proporciona un flujo de preguntas estructurado para evaluar diferentes tipos de lesiones dentales.

## ✨ Características

### 🤖 Inteligencia Artificial
- **Modelo:** GPT-2 / DistilGPT-2 usando Transformers
- **Generación automática** de opciones de respuesta contextuales
- **Respuestas inteligentes** basadas en el contexto de la conversación

### 🚨 Sistema de Recomendaciones Urgentes
- **Recomendación 1:** Avulsión dental - Conservación en leche/sales
- **Recomendación 2:** Fractura dental - Conservación en leche/sales  
- **Recomendación 3:** Luxación dental - Reposicionamiento
- **Recomendación 4:** Lesiones de tejidos blandos - Limpieza cuidadosa

### 🎯 Flujos de Conversación
- **Flujo para usuarios/pacientes:** Evaluación completa de trauma dental
- **Flujo para profesionales:** Orientación y asesoría especializada
- **Preguntas estructuradas** con respuestas de IA
- **Enlaces directos** a teleorientación y registro

### 🎨 Interfaz Profesional
- **Diseño universitario** con colores institucionales
- **Responsive design** para móviles y desktop
- **Indicadores de hablante** (🤖 ENtrauma / 👤 Usuario)
- **Estilos de advertencia** para recomendaciones urgentes
- **Enlaces clickeables** que se abren en nueva ventana

## 🚀 Instalación y Uso

### Requisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/jonathanAsias/chatbotEntrauma.git
cd chatbotEntrauma
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
```

3. **Activar entorno virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install flask transformers torch
```

5. **Ejecutar la aplicación:**
```bash
python entrauma_bot.py
```

6. **Acceder al chatbot:**
   - Abrir navegador en: `http://localhost:5003`

## 📁 Estructura del Proyecto

```
chatbotEntrauma/
├── entrauma_bot.py          # Aplicación principal Flask
├── templates/
│   └── entrauma.html        # Interfaz web del chatbot
├── static/
│   └── style.css           # Estilos CSS
├── README.md               # Documentación
└── requirements.txt        # Dependencias (crear si es necesario)
```

## 🔧 Configuración

### Variables de Entorno
- **Puerto:** 5003 (configurable en `entrauma_bot.py`)
- **Modelo IA:** GPT-2 (fallback a DistilGPT-2)

### Personalización
- **Preguntas:** Modificar `questions_flow` en `entrauma_bot.py`
- **Recomendaciones:** Editar `recommendations` en `entrauma_bot.py`
- **Estilos:** Personalizar CSS en `templates/entrauma.html`

## 🌐 Enlaces Importantes

- **Plataforma de registro:** https://www.entrauma.vortico.co/registrar-mis-datos
- **Correo de contacto:** entraumafo_bog@unal.edu.co
- **Atención al usuario:** atusuario_fobog@unal.edu.co

## 🏥 Información Médica

**IMPORTANTE:** Este chatbot es una herramienta de orientación inicial. En casos de emergencia dental, consulte inmediatamente con un profesional de la salud.

### Tipos de Trauma Cubiertos:
- **Avulsión:** Diente completamente fuera de la boca
- **Fractura:** Diente roto o partido
- **Luxación:** Diente desplazado de su posición
- **Lesiones de tejidos blandos:** Heridas en encías, labios, lengua

## 👥 Contribuciones

Este proyecto fue desarrollado para la Facultad de Odontología de la Universidad Nacional de Colombia. Para contribuciones o mejoras, contactar al equipo de desarrollo.

## 📄 Licencia

Proyecto desarrollado para uso académico y de investigación en la Universidad Nacional de Colombia.

## 🏛️ Universidad Nacional de Colombia

**Facultad de Odontología**  
**Servicio ENtrauma**  
*Especializado en trauma dental y bucal*

---

**Desarrollado con ❤️ para la comunidad universitaria**
