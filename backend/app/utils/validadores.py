import re

def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    for i in range(9, 11):
        valor = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        digito = ((value * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    
    return True