from fastapi import HTTPException
from datetime import datetime, timedelta
import secrets
import logging
from db.supabase import supabase_manager
from utils.sendmail import EmailSender
from models.user import PasswordReset, NewPasswordRequest

logger = logging.getLogger(__name__)

class PasswordController:
    def __init__(self):
        self.supabase = supabase_manager
        self.email_sender = EmailSender()

    async def create_reset_token(self, email: str) -> str:
        try:
            # Verificar si el usuario existe
            user_data = self.supabase.get_user_info(email)
            if not user_data.data:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Generar token aleatorio
            token = secrets.token_urlsafe(32)
            created_at = datetime.utcnow()
            expires_at = created_at + timedelta(minutes=30)

            # Guardar token en la base de datos
            self.supabase.save_reset_token(
                email=email,
                token=token,
                created_at=created_at.isoformat(),
                expires_at=expires_at.isoformat()
            )

            return token
        except Exception as e:
            logger.error(f"Error creating reset token: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al crear token de restablecimiento")

    async def verify_reset_token(self, token: str) -> str:
        try:
            result = self.supabase.get_reset_token(token)

            if not result.data:
                raise HTTPException(status_code=400, detail="Token inválido")

            token_data = result.data[0]
            expires_at = datetime.fromisoformat(token_data['expires_at'])

            if datetime.utcnow() > expires_at:
                # Eliminar token expirado
                self.supabase.delete_reset_token(token)
                raise HTTPException(status_code=400, detail="Token expirado")

            return token_data['email']
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error verifying reset token: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al verificar token")
        

    async def update_password(self, email: str, new_password: str):
        try:
            # Actualizar contraseña en el sistema de auth de Supabase
            self.supabase.update_user_password(email, new_password)

            # Eliminar el token usado
            self.supabase.delete_reset_token(email)

            return {"message": "Contraseña actualizada exitosamente"}
        except Exception as e:
            logger.error(f"Error updating password: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al actualizar contraseña")
    
    

