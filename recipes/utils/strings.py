def is_positive_number(value):
    try:
        number_str = float(value)

    except ValueError:
        return False
    
    return number_str > 0

