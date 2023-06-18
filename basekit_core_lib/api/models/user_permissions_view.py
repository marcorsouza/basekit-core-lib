from config.helpers import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import composite

Base = declarative_base()

class UserPermissions(Base):
    """
    Classe que representa a entidade mapeada para a view 'vw_user_permissions'.

    Atributos:
        task_id (int): ID da tarefa.
        role_id (int): ID da regra.
        action_id (int): ID da ação.
        user_id (int): ID do usuário.
        acronym (str): Acrônimo da aplicação.

        task_name (str): Nome da tarefa.
        tag_name (str): Tag da tarefa.
        role_name (str): Nome da regra.
        action_name (str): Nome da ação.
        name (str): Nome do usuário.
        username (str): Nome de usuário.
    """
    __tablename__ = 'vw_user_permissions'


    tag_name = Column(String(100), primary_key=True)
    action_name = Column(String(100), primary_key=True)
    username = Column(String(100), primary_key=True)
    acronym = Column(String(100), primary_key=True)

    task_id = Column(Integer)
    role_id = Column(Integer)
    action_id = Column(Integer)
    user_id = Column(Integer)
    task_name = Column(String(100))
    role_name = Column(String(100))
    name = Column(String(100))
    
    @staticmethod
    def get_user_permissions(username, tag_name, acronym, action_name):
        user_permissions = db.session.query(UserPermissions).filter_by(
            username=username,
            tag_name=tag_name,
            acronym=acronym,
            action_name=action_name
        ).first()

        return user_permissions
