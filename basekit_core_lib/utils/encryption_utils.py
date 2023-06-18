import bcrypt

def encrypt_value(value):
        """
        Criptografa um valor utilizando o algoritmo bcrypt.
        :param value: O valor a ser criptografado.
        :return: O valor criptografado.
        """
        salt = bcrypt.gensalt()
        hashed_value = bcrypt.hashpw(value.encode(), salt)
        return hashed_value.decode()
    
def is_encrypted(password, hashed_password):
    """
    Verifica se um valor está criptografado utilizando o algoritmo bcrypt.
    :param password: O valor a ser verificado.
    :param hashed_password: O hashed a ser comparado.
    :return: True se o valor está criptografado, False caso contrário.
    """
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())            
    except ValueError:
        return False
