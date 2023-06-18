import os
import importlib
os.urandom(32)

def get_key_generator(size):
    try:
        random_bytes = os.urandom(size)
    except Exception as e:
        print(f"Erro ao gerar key: {e}")
        return b'' 

    return random_bytes
    
def get_env(key, default=None):
    try:
        return os.getenv(key, default)
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne um valor alternativo
        #Logger().logger.error(f"Erro ao obter a variável de ambiente {key}: {e}")
        return default

def walk_directory(directory):
    try:
        return list(os.walk(directory))
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne um valor alternativo
        #Logger().logger.error(f"Erro ao percorrer o diretório {directory}: {e}")
        return []

def get_import_module(module_name):
    try:
        return importlib.import_module(module_name)
    except Exception as e:
        print(e)
        # Trate a exceção aqui, por exemplo, registre em log ou retorne um valor alternativo
        #Logger().logger.error(f"Erro ao importar o módulo {module_name}: {e}")
        return None

def get_attribute(obj, attr, default=None):
    try:
        return getattr(obj, attr, default)
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne um valor alternativo
        #Logger().logger.error(f"Erro ao obter o atributo {attr} do objeto {obj}: {e}")
        return default

def get_files(directory, name=None, contains=False):
    files = []
    
    try:
        for root, dirs, filenames in walk_directory(directory):
            for filename in filenames:
                if name:
                    if contains and name in filename:
                        files.append(os.path.join(root, filename))
                    elif not contains and name == filename:
                        files.append(os.path.join(root, filename))
                else:
                    files.append(os.path.join(root, filename))
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne uma lista vazia
        #Logger().logger.error(f"Erro ao obter os arquivos do diretório {directory}: {e}")
        return []
    
    return files

def get_filename(filepath):
    try:
        filename_with_extension = os.path.basename(filepath)
        filename, extension = os.path.splitext(filename_with_extension)
        return filename, extension
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne valores padrão
        # Logger().logger.error(f"Erro ao obter o nome do arquivo: {e}")
        return None, None
    
def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        # Logger().logger.info(f"Diretório criado: {directory}")
        return True
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne False
        # Logger().logger.error(f"Erro ao criar o diretório {directory}: {e}")
        return False

def directory_exists(directory):
    return os.path.exists(directory)

def create_file(filepath):
    try:
        with open(filepath, 'w') as file:
            pass
        # Logger().logger.info(f"Arquivo criado: {filepath}")
        return True
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne False
        # Logger().logger.error(f"Erro ao criar o arquivo {filepath}: {e}")
        return False

def load_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne None
        # Logger().logger.error(f"Erro ao carregar o arquivo {filepath}: {e}")
        return None

def delete_file(filepath):
    try:
        os.remove(filepath)
        # Logger().logger.info(f"Arquivo excluído: {filepath}")
        return True
    except Exception as e:
        # Trate a exceção aqui, por exemplo, registre em log ou retorne False
        # Logger().logger.error(f"Erro ao excluir o arquivo {filepath}: {e}")
        return False