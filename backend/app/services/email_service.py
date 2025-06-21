from flask_mail import Message
from ..extensions import mail
from ..models.usuario import Usuario

class EmailService:
    @staticmethod
    def enviar_email(to, subject, body):
        try:
            msg = Message(
                subject=subject,
                recipients=[to],
                body=body
            )
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        
    @staticmethod
    def enviar_email_de_confirmacao(usuario, medico, data_consulta):
        subject = "Confirmacao de agendamento - Saude DF"
        body = f"""Dear {usuario.name},

            Your appointment has been confirmed for {data_consulta.strftime('%Y-%m-%d %H:%M')} with Dr. {medico.name}.

            Best regards,
            Saúde DF Team"""
        return EmailService.enviar_email(usuario.email, subject, body)