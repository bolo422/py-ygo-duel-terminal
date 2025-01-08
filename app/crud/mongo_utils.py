def convert_all_dict_key_to_string(data):
    """Convert all keys in a dictionary to strings."""
    if isinstance(data, dict):
        return {str(k): convert_all_dict_key_to_string(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_all_dict_key_to_string(i) for i in data]
    return data