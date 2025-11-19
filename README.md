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

## 🐳 Instalación con Docker

### Docker Local

1. **Construir la imagen:**
```bash
docker build -t entrauma-chatbot .
```

2. **Ejecutar el contenedor:**
```bash
docker run -d -p 5003:5003 --name entrauma-chatbot --restart unless-stopped entrauma-chatbot
```

3. **Acceder al chatbot:**
   - Abrir navegador en: `http://localhost:5003`

### Docker en GCP (VM)

1. **Conectarse a la VM:**
```bash
gcloud compute ssh [NOMBRE_DE_LA_VM] --zone=[ZONA]
```

2. **Navegar al directorio del proyecto:**
```bash
cd ~/ChatbotRasa
```

3. **Verificar contenedores existentes:**
```bash
docker ps -a
```

4. **Si el contenedor ya existe:**
   - **Iniciar contenedor existente:**
   ```bash
   docker start entrauma-chatbot
   ```
   
   - **O eliminar y recrear:**
   ```bash
   docker rm -f entrauma-chatbot
   docker run -d -p 5003:5003 --name entrauma-chatbot --restart unless-stopped entrauma-chatbot
   ```

5. **⚠️ Configurar Firewall de GCP (IMPORTANTE):**
   
   Para acceder desde fuera de la VM, necesitas crear una regla de firewall que permita tráfico en el puerto 5003:
   
   **Opción A: Desde la consola de GCP (recomendado):**
   - Ve a **VPC Network** > **Firewall** en la consola de GCP
   - Click en **Create Firewall Rule**
   - Configura:
     - **Name:** `allow-entrauma-chatbot`
     - **Direction:** Ingress
     - **Targets:** All instances in the network (o selecciona tu VM específica)
     - **Source IP ranges:** `0.0.0.0/0` (para acceso público) o una IP específica
     - **Protocols and ports:** TCP, puerto `5003`
   - Click en **Create**
   
   **Opción B: Desde la línea de comandos:**
   ```bash
   gcloud compute firewall-rules create allow-entrauma-chatbot \
     --allow tcp:5003 \
     --source-ranges 0.0.0.0/0 \
     --description "Allow traffic to ENtrauma chatbot on port 5003"
   ```
   
   **Verificar reglas de firewall:**
   ```bash
   gcloud compute firewall-rules list | grep entrauma
   ```

6. **Verificar que el contenedor esté escuchando:**
```bash
# Desde dentro de la VM
docker logs entrauma-chatbot
netstat -tuln | grep 5003
```

7. **Acceder al chatbot:**
   - Desde fuera: `http://[IP_PUBLICA_DE_LA_VM]:5003`
   - Desde dentro de la VM: `http://localhost:5003`

8. **Comandos útiles de Docker:**
```bash
# Ver logs del contenedor
docker logs entrauma-chatbot

# Ver logs en tiempo real
docker logs -f entrauma-chatbot

# Detener el contenedor
docker stop entrauma-chatbot

# Reiniciar el contenedor
docker restart entrauma-chatbot

# Ver estado de contenedores
docker ps

# Ver todas las imágenes
docker images
```

### 🔍 Troubleshooting - Problemas de Construcción Docker

#### Error: `rpc error: code = Unavailable desc = error reading from server: EOF`

Este error indica que Docker perdió la conexión con el daemon durante la construcción. Soluciones:

1. **Verificar que Docker esté corriendo:**
```bash
# Windows
docker info

# Linux/Mac
sudo systemctl status docker
# O
docker info
```

2. **Reiniciar Docker:**
```bash
# Windows: Reiniciar Docker Desktop desde el menú
# Linux/Mac
sudo systemctl restart docker
```

3. **Limpiar recursos de Docker:**
```bash
# Limpiar imágenes, contenedores y caché
docker system prune -a

# Limpiar solo imágenes no utilizadas
docker image prune -a
```

4. **Verificar espacio en disco:**
```bash
# Windows: Verificar espacio en disco desde el explorador
# Linux/Mac
df -h
```

5. **Construir con más memoria/timeout:**
```bash
# Aumentar timeout y memoria disponible
docker build --network=host --memory=4g -t entrauma-chatbot .
```

6. **Construir sin caché (si hay problemas de caché corrupta):**
```bash
docker build --no-cache -t entrauma-chatbot .
```

7. **Construir en pasos (para identificar dónde falla):**
```bash
# Construir hasta una capa específica para aislar el problema
docker build --target [NOMBRE_DE_LA_CAPA] -t entrauma-chatbot .
```

8. **En Windows: Verificar configuración de Docker Desktop:**
   - Abrir Docker Desktop
   - Settings > Resources
   - Aumentar memoria asignada (mínimo 4GB recomendado)
   - Aumentar CPU asignada
   - Aplicar y reiniciar

9. **Si estás en una VM remota (GCP/AWS):**
```bash
# Verificar recursos disponibles
free -h
df -h

# Aumentar swap si es necesario
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 🔍 Troubleshooting - Problemas de Acceso

Si la aplicación se queda cargando o no responde desde la IP pública, verifica lo siguiente:

1. **Verificar que el contenedor esté corriendo:**
```bash
docker ps
# Debe mostrar entrauma-chatbot con estado "Up"
```

2. **Verificar que el puerto esté escuchando:**
```bash
sudo netstat -tuln | grep 5003
# O
sudo ss -tuln | grep 5003
# Debe mostrar: 0.0.0.0:5003 o :::5003
```

3. **Verificar el mapeo de puertos del contenedor:**
```bash
docker port entrauma-chatbot
# Debe mostrar: 5003/tcp -> 0.0.0.0:5003
```

4. **Probar desde dentro de la VM:**
```bash
curl http://localhost:5003
# Si funciona aquí pero no desde fuera = problema de firewall
```

5. **Verificar reglas de firewall de GCP:**
```bash
gcloud compute firewall-rules list | grep 5003
# O ver detalles:
gcloud compute firewall-rules describe allow-entrauma-chatbot
```

6. **Ver logs del contenedor:**
```bash
docker logs entrauma-chatbot --tail 50
# Busca errores o mensajes de conexión
```

7. **Probar conectividad desde fuera (máquina local):**
```bash
# Desde tu máquina local (no desde la VM):
curl -v http://[IP_PUBLICA]:5003
# O
telnet [IP_PUBLICA] 5003
```

8. **Verificar IP pública de la VM:**
```bash
# Desde la VM:
curl ifconfig.me
# O
gcloud compute instances describe instance-entrauma-chat --zone=[TU_ZONA] --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

**Problemas comunes:**
- ❌ **Se queda cargando:** Firewall de GCP no permite el puerto 5003 → Crear regla de firewall
- ❌ **Connection refused:** Contenedor no está corriendo → `docker start entrauma-chatbot`
- ❌ **Timeout:** Puerto no está mapeado correctamente → Verificar `docker port entrauma-chatbot`
- ❌ **Funciona localmente pero no desde fuera:** Problema de firewall → Verificar reglas de GCP

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
