from wtforms.validators import ValidationError

def validate_vin(form, field):
    vin = field.data.upper()

    if len(vin) != 17:
        raise ValidationError("VIN must be exactly 17 characters long.")

    invalid_chars = {'I', 'O', 'Q'}

    for char in vin:
        if not (char.isdigit() or char.isalpha()):
            raise ValidationError("VIN can only contain letters and numbers.")
        if char in invalid_chars:
            raise ValidationError("VIN contains invalid characters: I, O, and Q are not allowed.")

    # Dynamically use the model from the form
    model = getattr(form, "_model", None)
    if model and hasattr(model, "query"):
        existing_vin = model.query.filter_by(vin=vin).first()
        if existing_vin:
            raise ValidationError("VIN already exists.")

def validate_unique_username(form, field):
    username = field.data
    model = getattr(form, "_model", None)
    if model and hasattr(model, "query"):
        existing_user = model.query.filter_by(username=username).first()
        if existing_user:
            raise ValidationError("Username already exists. Please choose another.")

def validate_unique_email(form, field):
    email = field.data
    model = getattr(form, "_model", None)
    if model and hasattr(model, "query"):
        existing_user = model.query.filter_by(email=email).first()
        if existing_user:
            raise ValidationError("Email already exists. Please choose another.")
