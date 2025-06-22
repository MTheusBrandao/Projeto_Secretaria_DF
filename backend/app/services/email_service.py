from flask_mail import Message
from ..extensions import mail
from ..models.usuario import Usuario

class EmailService:
    @staticmethod
    def enviar_email(to, subject, body):
        
        print(f"Tentativa de enviar email para: {to}")  # Log para depuração
        print(f"Assunto: {subject}")
        print(f"Corpo: {body[:50]}...")  # Mostra apenas parte do corpo

        try:
            msg = Message(
                subject="Assunto fixo temporário",
                recipients=[to],
                body="Corpo fixo temporário"
            )

            mail.send(msg)
            return True
        except Exception as e:
            print(f"ERRO ao enviar email: {str(e)}")
            return False
        
    @staticmethod
    def enviar_email_de_confirmacao(usuario, medico, data_consulta):
        subject = "Confirmacao de agendamento - Saude DF"
        body = f"""Dear {usuario.name},

            Your appointment has been confirmed for {data_consulta.strftime('%Y-%m-%d %H:%M')} with Dr. {medico.name}.

            Best regards,
            Saúde DF Team"""
        return EmailService.enviar_email(usuario.email, subject, body)