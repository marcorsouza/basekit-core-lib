import os
from basekit_core_lib.api.services.base_service import BaseService
from basekit_admin_service.api.admin.models.user import User
from basekit_admin_service.api.admin.models.role import Role
from basekit_admin_service.api.admin.schemas import UserSchema,UserDetailSchema, UserUpdateSchema
from basekit_core_lib.config.helpers import db
from basekit_core_lib.utils.encryption_utils import encrypt_value, is_encrypted
from basekit_core_lib.utils.generate_random_password import generate_random_password

from datetime import datetime, timedelta

class UserService(BaseService):
    def __init__(self) -> None:
        super().__init__(User, UserSchema())
        self.user_detail_schema = UserDetailSchema()
        self.user_upd_schema = UserUpdateSchema()
        
    def get_all(self):
        try:
            models = self._get_all()            
            model_data = self.user_detail_schema.dump(models, many=True)
            return model_data
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao obter todos os usuários: {e}")
        
    def paged_list(self , filters =  None):
        try:
            models, total_count = self._paged_list(filters)            
            model_data = self.user_detail_schema.dump(models, many=True)
            return model_data, total_count
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao obter todos os usuários: {e}")

    def get_by_id(self, id):
        try:
            model = self._get_by_id(id)
            if model:
                model_data = self.user_detail_schema.dump(model)
                return model_data
            return None
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao obter usuário por ID {id}: {e}")
        
    
    def create(self, model_data):
        try:
            self.is_valid(self.model_schema, model_data)  # Valida o schema antes de criar o usuário
            model_data = self.model_schema.load(model_data)        
            model_data['password'] = encrypt_value(model_data['password'])
                      
            model = self._create(model_data)
            model_data = self.user_detail_schema.dump(model)
            
            return model_data
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao criar usuário: {e}")
    
    def update(self, id, model_data):
        try:            
            self.is_valid(self.user_upd_schema, model_data) # Valida o schema antes de atualizar o usuário
            model = User.query.get(id)
            model.last_change = datetime.utcnow()
            
            if model:
                self._update(model, model_data, self.user_upd_schema)
                model_data = self.user_detail_schema.dump(model)
                return model_data
            return None
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao atualizar usuário com ID {id}: {e}")

    def delete(self, id):
        try:
            return self._delete(id)
        except Exception as e:
            db.session.rollback()  # Executa o rollback para reverter a transação
            raise Exception(f"Erro ao excluir usuário com ID {id}: {e}")
        
    def recovery_password(self, model_data):
        # Lógica para recuperar a senha do usuário com base no email
        # Envio de email com instruções para redefinição da senha
        try: 
            email = model_data.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                new_pass = generate_random_password()
                user.temporary_password = encrypt_value(new_pass)
                expiration_time = datetime.utcnow() + timedelta(hours=self.config.TEMPORARY_PASSWORD_EXPIRATION)
                user.temporary_password_expiration = expiration_time
                db.session.commit()
            else:
                return None
            return {"message": 'New Password', "new_password": new_pass}
        except Exception as e:
            raise Exception(f"Erro ao recuperar senha: {e}")

    def change_password(self, id, model_data):        
        try:        
            password = model_data.get('password')
            confirm_password = model_data.get('confirm_password')
            if password == confirm_password:
                # As senhas coincidem, podemos prosseguir com a alteração
                hashed_password = encrypt_value(password)
                model = User.query.get(id)
                if model:
                    model.password = hashed_password
                    db.session.commit()
                    return {"message": 'Senha alterada com sucesso!'}
                return None
            else:
                return False  # Indica que a alteração de senha falhou
        except Exception as e:
            raise Exception(f"Erro ao alterar senha: {e}")
        
    def add_roles_to_user(self, user_id, model_data):
        try:
            user = User.query.get(user_id)
            
            if user is None:
                return False

            roles = model_data.get('roles', [])
            for role in roles:
                role_id = role.get('id')
                if role_id is not None and role_id not in user.roles:
                    new_role = Role.query.get(role_id)
                    user.roles.append(new_role)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
        
    def del_roles_to_user(self, user_id, model_data):
        try:
            user = User.query.get(user_id)
            if user is None:
                return False

            roles = model_data.get('roles', [])
            for role in roles:
                role_id = role.get('id')
                if role_id is not None and role_id not in user.roles:
                    del_role = Role.query.get(role_id)
                    user.roles.remove(del_role)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
