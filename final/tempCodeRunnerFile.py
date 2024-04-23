def validate_YYYYMMDDHHMMSS(value, field_name):
    pattern = r'^\d{14}$'
    if not re.match(pattern, value):
        return f"{field_name} does not match the YYYYMMDDHHMMSS format."
    try:
        datetime.strptime(value, '%Y%m%d%H%M%S')
    except ValueError:
        return f"{field_name} is not a valid datetime."
    return None