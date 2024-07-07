def validate_user_data(data):
    errors = []
    required_fields = ["firstName", "lastName", "email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append({"field": field, "message": f"{field} is required."})

    if errors:
        return errors
    return None