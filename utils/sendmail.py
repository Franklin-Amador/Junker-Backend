import yagmail
import logging
from fastapi import FastAPI, HTTPException
from models.user import MailSend
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD

app = FastAPI()

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.email_sender = yagmail.SMTP(
            user=EMAIL_USERNAME,
            password=EMAIL_PASSWORD
        )
    async def send_reset_email(self, email: str, token: str):
  
        try:
            # URL base de tu frontend
            base_url = "https://tu-sitio.com"  # Cambia esto por tu URL real
            reset_link = f"{base_url}/reset-password?token={token}"
            
            # Contenido del correo
            subject = "Restablecimiento de contraseña"
            contents = [
                "<h2>Restablecimiento de contraseña</h2>",
                f"<p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:</p>",
                f"<p><a href='{reset_link}'>Restablecer contraseña</a></p>",
                "<p><strong>Este enlace expirará en 3 minutos.</strong></p>",
                "<p>Si no solicitaste este cambio, por favor ignora este correo.</p>",
                "<br>",
                "<p>Por razones de seguridad, este enlace solo funcionará una vez. " 
                "Si necesitas restablecer tu contraseña nuevamente, deberás solicitar un nuevo enlace.</p>",
                "<hr>",
                "<p><small>Este es un correo automático, por favor no respondas a este mensaje.</small></p>"
            ]

            # Enviar el correo
            self.email_sender.send(
                to=email,
                subject=subject,
                contents=contents
            )
            
            logger.info(f"Password reset email sent successfully to {email}")
            
        except Exception as e:
            error_msg = f"Error sending reset email to {email}: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=500,
                detail="Error al enviar el correo de restablecimiento"
            )

    async def send_success_email(self, email: str):
        """
        Envía un correo de confirmación cuando la contraseña ha sido cambiada exitosamente.
        
        Args:
            email (str): Dirección de correo del usuario
            
        Raises:
            HTTPException: Si hay un error al enviar el correo
        """
        try:
            subject = "Contraseña actualizada exitosamente"
            contents = [
                "<h2>Contraseña actualizada</h2>",
                "<p>Tu contraseña ha sido actualizada exitosamente.</p>",
                "<p>Si no realizaste este cambio, por favor contacta inmediatamente con soporte.</p>",
                "<br>",
                "<p><small>Este es un correo automático, por favor no respondas a este mensaje.</small></p>"
            ]

            self.email_sender.send(
                to=email,
                subject=subject,
                contents=contents
            )
            
            logger.info(f"Success confirmation email sent to {email}")
            
        except Exception as e:
            error_msg = f"Error sending success email to {email}: {str(e)}"
            logger.error(error_msg)

# * Función para enviar el correo de bienvenida 
async def welcome_email(email: MailSend):
    try:
        # Configurar yagmail
        yag = yagmail.SMTP(EMAIL_USERNAME, EMAIL_PASSWORD)

        # Enviar el correo
        subject = "Bienvenido a nuestra plataforma Junker"
        contents = f"Gracias por unirte a nuestra familia."
                
        yag.send(to=email, subject=subject, contents=contents)
                
        print("Correo de bienvenida enviado con éxito")
        return {"success": True, "message": "Correo de bienvenida enviado"}

    except Exception as e:
        print(f"Error al enviar el correo de bienvenida: {e}")
        return {"success": False, "message": f"Error al enviar el correo de bienvenida: {str(e)}"}
    
# * Funicón para  enviar mail de forgot password
async def forgot_password(email: MailSend):
    try:
        yag = yagmail.SMTP(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        subject = "Reestablecer contraseña"
        contents = "El enlace para reestablecer contraseña tiene una validez de 3 minutos y es de un uso único."
        
        yag.send(to=email, subject=subject, contents=contents)
        
        print("Correo de reestablecimiento enviado exitosamente")
        return {"success":True, "message": "Correo enviado"}
     
    except Exception as e:
        print(f"Error al enviar el correo de bienvenida: {e}")
        return {"success": False, "message": f"Error al enviar el correo de bienvenida: {str(e)}"}
    
# ? Funcíón para el forgot...
async def send_reset_email(self, email: str, token: str):
        try:
            reset_link = f"https://tu-sitio.com/reset-password?token={token}"
            contents = [
                "Restablecimiento de contraseña",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}",
                "Este enlace expirará en 3 minutos.",
                "Si no solicitaste este cambio, ignora este correo."
            ]
            
            self.email_sender.send(
                to=email,
                subject="Restablecimiento de contraseña",
                contents=contents
            )
        except Exception as e:
            raise Exception(f"Error al enviar correo de restablecimiento: {e}")