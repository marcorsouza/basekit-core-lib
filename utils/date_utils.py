def format_date(date, format="%Y-%m-%d"):
    try:
        return date.strftime(format)
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne uma string vazia
        # Logger().logger.error(f"Erro ao formatar a data: {e}")
        return ""