![{0644F0C0-ED15-46F9-A89E-AA63D351FB03}](https://github.com/user-attachments/assets/969636cc-101b-4847-b578-41d428fd963a)


# 🤖 AntiBoomerBot

**AntiBoomerBot** es un bot de Discord diseñado para proteger servidores de spam, abusos y mensajes no deseados de forma automática y eficiente.

---

## 🚀 Características principales
- 🛡️ **Detección de spam** en múltiples canales: Si un usuario envía el mismo mensaje repetidamente en diferentes canales en un corto periodo de tiempo, será baneado automáticamente.
- 📢 **Detección de abusos de @everyone**: Detecta si un usuario menciona `@everyone` repetidamente en menos de 15 segundos.
- 🚫 **Detección de palabras clave peligrosas**: Monitorea mensajes que contengan palabras como "FREE" para prevenir estafas.
- 🔨 **Baneo automático**: Banea usuarios que incumplan las normas de spam.
- 🧹 **Eliminación de mensajes**: Borra todos los mensajes del usuario baneado de las últimas 24 horas.
- 📬 **Sistema de notificaciones**: Puedes configurar un webhook opcional para recibir alertas de acciones automáticas.
- ⚙️ **Fácil activación**: Solo usa `/iniciar` y el bot empezará a proteger tu servidor.
- 🔐 **Solo administradores** pueden activar/configurar, sin necesidad de editar el código.

---

## 📜 Comandos disponibles
- `/iniciar` — Activa el sistema AntiBoomer en el servidor.
- `/avisos [webhook_url]` — Configura un webhook donde se enviarán las notificaciones de baneos.

---

## 🧩 Requisitos
- 🐍 Python 3.9 o superior.
- 📚 Librerías necesarias:
  - `discord.py` versión 2.3.2 o superior.
  - `aiohttp` versión 3.8.6 o superior.

---

## 🛠️ Instalación paso a paso

```bash
# 📥 Clona este repositorio
git clone https://github.com/Kayy9961/Bot-Anti-Boomer.git

# 📂 Entra al directorio
cd Bot-Anti-Boomer

# 📦 Instala las dependencias necesarias
pip install -r requirements.txt

# 🛠️ (Opcional) Crea un archivo .env o configura tu token directamente en el código

# 🚀 Ejecuta el bot
python main.py
