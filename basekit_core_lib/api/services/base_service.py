from abc import ABC, abstractmethod
from basekit_core_lib.api.services.filter_builder import FilterBuilder
from basekit_core_lib.config.helpers import db, config
from sqlalchemy import or_,and_, not_, func
from typing import Optional

class BaseService(ABC):
    
    def __init__(self,model_data: db.Model = None, model_schema = None) -> None:
        self.model_data = model_data
        self.model_schema = model_schema
        self.filter_builder = FilterBuilder(model_data)
        self.config  = config
        
    def _get_all(self, filters=None):
        query = self.model_data.query

        if filters:
            for field, value in filters.items():
                query = self._apply_filter(query, field, value)

        results = query.all()
        print(query.statement)
        return results

    def _apply_filter(self, query, field, value):
        if field == "or" or field == "and":
            return self.apply_logical_filter(query, field, self.filter_builder.build_logical_filters(value))
        elif field not in ["in", "like", "eq", "not", "not_in", "gt", "lt", "between", "isNull"]:
            raise ValueError(f"Campo de filtro inválido: {field}")

        if field == "in":
            return self.apply_in_filter(query, value)
        elif field == "not_in":
            return self.apply_not_in_filter(query, value)
        elif field == "gt":
            return self.apply_gt_filter(query, value)
        elif field == "lt":
            return self.apply_lt_filter(query, value)
        elif field == "between":
            return self.apply_between_filter(query, value)
        elif field == "isNull":
            return self.apply_is_null_filter(query, value)
        elif field == "like":
            return self.apply_like_filter(query, value)
        elif field in ["eq", "equal", "equals"]:
            return self.apply_eq_filter(query, value)
        elif field == "not":
            return self.apply_not_filter(query, value)
        else:
            return self.apply_eq_filter(query, {field: value})

    def apply_logical_filter(self, query, operator, filters):
        if operator == "or":
            return query.filter(or_(*filters))
        elif operator == "and":
            return query.filter(and_(*filters))
        else:
            raise ValueError(f"Operador lógico inválido: {operator}")

    def apply_in_filter(self, query, value):
        """
        Aplica o filtro 'in' em um campo específico.
        
        O filtro 'in' é utilizado para buscar registros cujo valor de um campo esteja contido em uma lista de valores fornecida.
        
        Exemplo:
        filters = {
            "in": {"id": [1, 2, 3]}
        }
        query = apply_in_filter(query, filters)
        
        Esse exemplo aplica o filtro 'in' no campo 'id', buscando por registros cujo valor esteja na lista [1, 2, 3].
        """
        for attr_filter in self.filter_builder.build_in_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_not_in_filter(self, query, value):
        """
        Aplica o filtro 'not_in' em um campo específico.
        
        O filtro 'not_in' é utilizado para buscar registros cujo valor de um campo não esteja contido em uma lista de valores fornecida.
        
        Exemplo:
        filters = {
            "not_in": {"id": [4, 5, 6]}
        }
        query = apply_not_in_filter(query, filters)
        
        Nesse exemplo, é aplicado o filtro 'not_in' no campo 'id', buscando por registros cujo valor não esteja na lista [4, 5, 6].
        """
        for attr_filter in self.filter_builder.build_not_in_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_gt_filter(self, query, value):
        """
        Aplica o filtro 'gt' (maior que) em um campo específico.
        
        O filtro 'gt' é utilizado para buscar registros cujo valor de um campo seja maior que um valor fornecido.
        
        Exemplo:
        filters = {
            "gt": {"id": 10}
        }
        query = apply_gt_filter(query, filters)
        
        Esse exemplo aplica o filtro 'gt' no campo 'id', buscando por registros cujo valor seja maior que 10.
        """
        for attr_filter in self.filter_builder.build_gt_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_lt_filter(self, query, value):
        """
        Aplica o filtro 'lt' (menor que) em um campo específico.
        
        O filtro 'lt' é utilizado para buscar registros cujo valor de um campo seja menor que um valor fornecido.
        
        Exemplo:
        filters = {
            "lt": {"id": 5}
        }
        query = apply_lt_filter(query, filters)
        
        Nesse exemplo, é aplicado o filtro 'lt' no campo 'id', buscando por registros cujo valor seja menor que 5.
        """
        for attr_filter in self.filter_builder.build_lt_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_between_filter(self, query, value):
        """
        Aplica o filtro 'between' em um campo específico.
        
        O filtro 'between' é utilizado para buscar registros cujo valor de um campo esteja entre dois valores fornecidos.
        
        Exemplo:
        filters = {
            "between": {"id": [5, 10]}
        }
        query = apply_between_filter(query, filters)
        
        Esse exemplo aplica o filtro 'between' no campo 'id', buscando por registros cujo valor esteja entre 5 e 10.
        """
        for attr_filter in self.filter_builder.build_between_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_is_null_filter(self, query, value):
        """
        Aplica o filtro 'isNull' em um campo específico.
        
        O filtro 'isNull' é utilizado para buscar registros em que o valor de um campo seja nulo (None).
        
        Exemplo:
        filters = {
            "isNull": {"last_login_date": True}
        }
        query = apply_is_null_filter(query, filters)
        
        Nesse exemplo, é aplicado o filtro 'isNull' no campo 'last_login_date', buscando por registros em que o valor seja nulo.
        """
        for attr_filter in self.filter_builder.build_is_null_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_like_filter(self, query, value):
        """
        Aplica o filtro 'like' em um campo específico.
        
        O filtro 'like' é utilizado para buscar registros cujo valor de um campo contenha uma determinada substring fornecida.
        
        Exemplo:
        filters = {
            "like": {"name": "John"}
        }
        query = apply_like_filter(query, filters)
        
        Esse exemplo aplica o filtro 'like' no campo 'name', buscando por registros em que o valor contenha a substring "John".
        """
        for attr_filter in self.filter_builder.build_like_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_eq_filter(self, query, value):
        """
        Aplica o filtro 'eq' (igual a) em um campo específico.
        
        O filtro 'eq' é utilizado para buscar registros cujo valor de um campo seja igual a um valor fornecido.
        
        Exemplo:
        filters = {
            "eq": {"age": 25}
        }
        query = apply_eq_filter(query, filters)
        
        Nesse exemplo, é aplicado o filtro 'eq' no campo 'age', buscando por registros em que o valor seja igual a 25.
        """
        for attr_filter in self.filter_builder.build_eq_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_not_filter(self, query, value):
        """
        Aplica o filtro 'not' em um campo específico.
        
        O filtro 'not' é utilizado para buscar registros cujo valor de um campo seja diferente de um valor fornecido.
        
        Exemplo:
        filters = {
            "not": {"status": "inactive"}
        }
        query = apply_not_filter(query, filters)
        
        Esse exemplo aplica o filtro 'not' no campo 'status', buscando por registros em que o valor seja diferente de "inactive".
        """
        for attr_filter in self.filter_builder.build_not_filters(value):
            query = query.filter(attr_filter)
        return query
        
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