from abc import ABC, abstractmethod
from basekit_core_lib.utils.filter_builder import FilterBuilder
from basekit_core_lib.config.helpers import db, config
from sqlalchemy import or_,and_, not_, func
from typing import Optional


class BaseService(ABC):
    """
    Classe base para serviços que realizam operações CRUD em um modelo de dados SQLAlchemy.
    Os métodos a seguir precisam ser implementados pelas classes derivadas.

    Métodos abstratos:
        - get_all(): Retorna todos os registros do modelo.
        - get_by_id(id): Retorna um registro específico do modelo pelo ID.
        - create(): Cria um novo registro do modelo.
        - update(id): Atualiza um registro existente do modelo pelo ID.
        - delete(id): Exclui um registro existente do modelo pelo ID.
    """
    
    def __init__(self,model_data: db.Model = None, model_schema = None) -> None:
        self.model_data = model_data
        self.model_schema = model_schema
        self.filter_builder = FilterBuilder(model_data)
        self.config  = config
        
    def _get_all(self, filters=None):
        """
        Método interno para obter todos os registros do modelo com base nos filtros fornecidos.

        Args:
            filters (dict): Um dicionário contendo os filtros a serem aplicados na consulta.

        Returns:
            results: Uma lista contendo todos os registros do modelo que atendem aos filtros especificados.
        """
        
        query = self.model_data.query
        pagination = None
        if filters:
            for field, value in filters.items():
                if field == "order_by":
                    query = self._apply_order_by(query, value)
                elif field == "pagination":
                    pagination = value
                else:
                    for _field, val in value.items():
                        query = self._apply_filter(query, _field, val)

        if not pagination is None:
            return self._apply_pagination(query, pagination)
        
        results = query.all()
        print(query.statement)
        
        return results
    
    def _apply_pagination(self, query, pagination):
        """
        Método interno para aplicar a paginação aos resultados da consulta.

        Args:
            query: A consulta SQLAlchemy na qual a paginação será aplicada.
            pagination (dict): Um dicionário contendo informações sobre a paginação.

        Returns:
            results: Uma lista contendo os resultados paginados da consulta.
        """
        
        try:
            page = pagination.get('page', 1)
            per_page = pagination.get('per_page', 10)
            
            if page <= 0:
                page = 1
            if per_page <= 0:
                per_page = 10
            
            print(page)
            print(per_page)
            paginated_query = query.paginate(page=page, per_page=per_page)            
            results = paginated_query.items
            print(query.statement)
            return results
        except Exception as e:
            return None
    
    def _apply_order_by(self, query, order_by):
        """
        Método interno para aplicar a ordenação aos resultados da consulta.

        Args:
            query: A consulta SQLAlchemy na qual a ordenação será aplicada.
            order_by (list): Uma lista de dicionários contendo informações sobre a ordenação.

        Returns:
            query: A consulta SQLAlchemy com a ordenação aplicada.
        """
        
        for order in order_by:
            field = order.get("field")
            order_type = order.get("order", "asc")  # Valor padrão "asc" se não for especificado

            if field:
                column = getattr(self.model_data, field)
                if order_type == "desc":
                    column = column.desc()

                query = query.order_by(column)

        return query

    def _apply_filter(self, query, field, value):
        """
        Método interno para aplicar um filtro específico à consulta.

        Args:
            query: A consulta SQLAlchemy à qual o filtro será aplicado.
            field (str): O campo no qual o filtro será aplicado.
            value: O valor a ser usado no filtro.

        Returns:
            query: A consulta SQLAlchemy com o filtro aplicado.
        """
        field = field.lower()  # Converte o campo para letras minúsculas
        
        if field == "or" or field == "and":
            return self.apply_logical_filter(query, field, self.filter_builder.build_logical_filters(value))
        elif field not in ["in", "like", "eq", "not", "not_in", "gt", "lt", "between", "isnull"]:
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
        elif field == "isnull":
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
        """
        Método para aplicar um filtro lógico (AND/OR) à consulta.

        Args:
            query: A consulta SQLAlchemy à qual o filtro será aplicado.
            operator (str): O operador lógico a ser aplicado ("and" ou "or").
            filters (list): Uma lista de filtros a serem aplicados com o operador lógico.

        Returns:
            query: A consulta SQLAlchemy com o filtro lógico aplicado.
        """
        
        if operator == "or":
            return query.filter(or_(*filters))
        elif operator == "and":
            return query.filter(and_(*filters))
        else:
            raise ValueError(f"Operador lógico inválido: {operator}")

    def apply_in_filter(self, query, value):
        for attr_filter in self.filter_builder.build_in_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_not_in_filter(self, query, value):
        for attr_filter in self.filter_builder.build_not_in_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_gt_filter(self, query, value):
        for attr_filter in self.filter_builder.build_gt_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_lt_filter(self, query, value):
        for attr_filter in self.filter_builder.build_lt_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_between_filter(self, query, value):
        for attr_filter in self.filter_builder.build_between_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_is_null_filter(self, query, value):
        for attr_filter in self.filter_builder.build_is_null_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_like_filter(self, query, value):
        for attr_filter in self.filter_builder.build_like_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_eq_filter(self, query, value):
        for attr_filter in self.filter_builder.build_eq_filters(value):
            query = query.filter(attr_filter)
        return query

    def apply_not_filter(self, query, value):
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