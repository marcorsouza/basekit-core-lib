from abc import ABC, abstractmethod
from basekit_core_lib.config.helpers import db, config
class BaseService(ABC):
    
    def __init__(self,model_data: db.Model = None, model_schema = None) -> None:
        self.model_data = model_data
        self.model_schema = model_schema
        self.config  = config
    
    def _get_all(self):
        return self.model_data.query.all()

    def _get_by_id(self, id):
        return self.model_data.query.get(id)
    
    def _create(self, model_data):
        model = self.model_data(**model_data)        
        db.session.add(model)
        db.session.commit()
        return model
    
    def _update(self, model, model_data, schema_update = None):        
        if schema_update is None:
            schema_update = self.model_schema
        
        for key, value in model_data.items():
            if key in schema_update.fields:  # Verifica se o campo está presente no esquema de atualização
                setattr(model, key, value)
        db.session.commit()

    def _delete(self, id):
        model = self._get_by_id(id)
        if model:
            db.session.delete(model)
            db.session.commit()
            return True
        return False
    
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self, id):
       pass

    @abstractmethod
    def delete(self, id):
        pass
    
    def is_valid(self, model_schema, model_data):
        errors = model_schema.validate(model_data)
        if errors:
            ValueError(errors)
        return True