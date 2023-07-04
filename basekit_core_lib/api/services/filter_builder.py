class FilterBuilder:
    def __init__(self, model_data):
        self.model_data = model_data

    def get_attr(self, subfield):
        return getattr(self.model_data, subfield)

    def build_filter(self, operator, value):
        filters = []

        for field, val in value.items():
            if operator == "like":
                filters.append(self.get_attr(field).like(f"%{val}%"))
            elif operator == "eq":
                filters.append(self.get_attr(field) == val)
            elif operator == "not":
                filters.append(self.get_attr(field) != val)
            elif operator == "in":
                filters.append(self.get_attr(field).in_(val))
            elif operator == "not_in":
                filters.append(self.get_attr(field).notin_(val))
            elif operator == "gt":
                filters.append(self.get_attr(field) > val)
            elif operator == "lt":
                filters.append(self.get_attr(field) < val)
            elif operator == "between":
                filters.append(self.get_attr(field).between(val[0], val[1]))
            elif operator == "isNull":
                if isinstance(val, str):
                    filters.append(self.get_attr(val).is_(None))
                else:
                    if val:
                        filters.append(self.get_attr(field).is_(None))
                    else:
                        filters.append(self.get_attr(field).isnot(None))
            else:
                raise ValueError(f"Operador de filtro inválido: {operator}")

        return filters

    def build_logical_filters(self, value):
        filters = []

        for subfield, subvalue in value.items():
            if subfield == "like":
                filters.extend(self.build_like_filters(subvalue))
            elif subfield == "eq":
                filters.extend(self.build_eq_filters(subvalue))
            elif subfield == "not":
                filters.extend(self.build_not_filters(subvalue))
            elif subfield == "in":
                filters.extend(self.build_in_filters(subvalue))
            elif subfield == "not_in":
                filters.extend(self.build_not_in_filters(subvalue))
            elif subfield == "gt":
                filters.extend(self.build_gt_filters(subvalue))
            elif subfield == "lt":
                filters.extend(self.build_lt_filters(subvalue))
            elif subfield == "between":
                filters.extend(self.build_between_filters(subvalue))
            elif subfield == "isNull":
                filters.extend(self.build_is_null_filters(subvalue))
            else:
                raise ValueError(f"Campo de filtro inválido: {subfield}")

        return filters

    def build_like_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field).like(f"%{val}%"))

        return filters

    def build_eq_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field) == val)

        return filters

    def build_not_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field) != val)

        return filters

    def build_in_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field).in_(val))

        return filters

    def build_not_in_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field).notin_(val))

        return filters

    def build_gt_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field) > val)

        return filters

    def build_lt_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field) < val)

        return filters

    def build_between_filters(self, value):
        filters = []

        for field, val in value.items():
            filters.append(self.get_attr(field).between(val[0], val[1]))

        return filters

    def build_is_null_filters(self, value):
        filters = []

        if isinstance(value, str):
            filters.append(self.get_attr(value).is_(None))
        else:
            for field, is_null in value.items():
                if is_null:
                    filters.append(self.get_attr(field).is_(None))
                else:
                    filters.append(self.get_attr(field).isnot(None))

        return filters