import json


def serialize(data):
    try:
        return json.dumps(data)
    except TypeError as e:
        raise ValueError(f"Error al serializar los datos: {str(e)}")


def deserialize(json_data):
    try:
        return json.loads(json_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al deserializar los datos: {str(e)}")