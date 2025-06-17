def enviar_email(destinatario, assunto, corpo):
    try:
        print(f"[EMAIL SIMULADO] Para: {destinatario} | Assunto: {assunto}")
        print(corpo)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
