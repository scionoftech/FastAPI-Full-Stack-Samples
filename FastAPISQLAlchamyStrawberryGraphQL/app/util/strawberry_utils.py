import re
import strawberry


def convert_strawberry_to_dict_return_non_null(strawberry_model):
    """

    """

    data_dict = strawberry.asdict(strawberry_model)
    non_null_values = {}
    for key, value in data_dict.items():
        if value is not None and key not in ["id", "password"]:
            non_null_values[key] = value
    return non_null_values


def convert_camel_case(name):
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    name = pattern.sub("_", name).lower()
    return name


def get_only_selected_fields(db_baseclass_nname, info):
    """

    """

    db_relations_fields = inspect(
        db_baseclass_nname).relationships.keys()
    selected_fields = [convert_camel_case(field.name) for field in
                       info.selected_fileds[0].selections if
                       field.name not in db_relations_fields]

    return selected_fields


def get_valid_data(model_data_object, model_calss):
    data_dict = {}

    for column in model_calss.__table__.columns:
        try:
            data_dict[column.name] = getattr(model_data_object,
                                             column.name)
        except:
            pass
    return data_dict


def params_to_string_in_dict_format(**kwargs):
    params_string = "\n".join(
        f"{''.join(key.split('_'))}: {value}" for key, value in
        kwargs.items())
    return params_string


