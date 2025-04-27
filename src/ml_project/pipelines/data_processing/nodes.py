def load_data() -> dict:
    data = {
        "name": ["Alice", "Bob", "Charlie", None],
        "age": [25, 30, None, 22],
    }
    return data


def clean_data(data: dict) -> dict:
    # Remove entries where name or age is None
    clean_name = [n for n in data["name"] if n is not None]
    clean_age = [a for a in data["age"] if a is not None]

    cleaned_data = {"name": clean_name, "age": clean_age}
    return cleaned_data
