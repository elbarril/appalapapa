"""
Flask-WTF forms for all application operations.

All forms include CSRF protection and validation.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    DecimalField,
    DateField,
    SelectField,
    TextAreaField,
    BooleanField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    NumberRange,
    Optional,
    ValidationError,
)

from app.utils.constants import (
    MIN_PASSWORD_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PRICE,
    MIN_PRICE,
)


# =============================================================================
# Authentication Forms
# =============================================================================


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido."),
            Email(message="Ingresa un email válido."),
        ],
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired(message="La contraseña es requerida.")]
    )
    remember_me = BooleanField("Recordarme")


class RegistrationForm(FlaskForm):
    """User registration form."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido."),
            Email(message="Ingresa un email válido."),
            Length(max=255, message="El email es demasiado largo."),
        ],
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es requerida."),
            Length(
                min=MIN_PASSWORD_LENGTH,
                message=f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(message="Confirma tu contraseña."),
            EqualTo("password", message="Las contraseñas deben coincidir."),
        ],
    )

    def validate_password(self, field):
        """Custom password strength validation."""
        password = field.data
        if password:
            # Check for at least one letter and one number
            has_letter = any(c.isalpha() for c in password)
            has_number = any(c.isdigit() for c in password)

            if not (has_letter and has_number):
                raise ValidationError(
                    "La contraseña debe contener al menos una letra y un número."
                )


class ResetPasswordRequestForm(FlaskForm):
    """Password reset request form."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido."),
            Email(message="Ingresa un email válido."),
        ],
    )


class ResetPasswordForm(FlaskForm):
    """Password reset form with security question (legacy)."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido."),
            Email(message="Ingresa un email válido."),
        ],
    )
    new_password = PasswordField(
        "Nueva Contraseña",
        validators=[
            DataRequired(message="La nueva contraseña es requerida."),
            Length(
                min=MIN_PASSWORD_LENGTH,
                message=f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(message="Confirma tu contraseña."),
            EqualTo("new_password", message="Las contraseñas deben coincidir."),
        ],
    )
    security = StringField(
        "Pregunta de Seguridad",
        validators=[DataRequired(message="La respuesta de seguridad es requerida.")],
    )


class ChangePasswordForm(FlaskForm):
    """Change password form for logged-in users."""

    current_password = PasswordField(
        "Contraseña Actual",
        validators=[DataRequired(message="Ingresa tu contraseña actual.")],
    )
    new_password = PasswordField(
        "Nueva Contraseña",
        validators=[
            DataRequired(message="La nueva contraseña es requerida."),
            Length(
                min=MIN_PASSWORD_LENGTH,
                message=f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar Nueva Contraseña",
        validators=[
            DataRequired(message="Confirma tu nueva contraseña."),
            EqualTo("new_password", message="Las contraseñas deben coincidir."),
        ],
    )


# =============================================================================
# Patient Forms
# =============================================================================


class PersonForm(FlaskForm):
    """Form for creating/editing a patient."""

    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es requerido."),
            Length(
                min=2,
                max=MAX_NAME_LENGTH,
                message=f"El nombre debe tener entre 2 y {MAX_NAME_LENGTH} caracteres.",
            ),
        ],
    )
    notes = TextAreaField(
        "Notas",
        validators=[
            Optional(),
            Length(
                max=1000,
                message="Las notas son demasiado largas (máximo 1000 caracteres).",
            ),
        ],
    )


class DeletePersonForm(FlaskForm):
    """Confirmation form for deleting a patient."""

    person_id = HiddenField("ID", validators=[DataRequired()])
    confirm = BooleanField(
        "Confirmo que deseo eliminar este paciente",
        validators=[DataRequired(message="Debes confirmar para eliminar.")],
    )


# =============================================================================
# Session Forms
# =============================================================================


class SessionForm(FlaskForm):
    """Form for creating a new therapy session."""

    person_id = SelectField(
        "Paciente",
        coerce=int,
        validators=[DataRequired(message="Selecciona un paciente.")],
    )
    session_date = DateField(
        "Fecha", validators=[DataRequired(message="La fecha es requerida.")]
    )
    session_price = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(message="El precio es requerido."),
            NumberRange(
                min=MIN_PRICE,
                max=MAX_PRICE,
                message=f"El precio debe estar entre ${MIN_PRICE} y ${MAX_PRICE:,.0f}.",
            ),
        ],
    )
    pending = BooleanField("Pago Pendiente", default=True)
    notes = TextAreaField(
        "Notas",
        validators=[
            Optional(),
            Length(
                max=500,
                message="Las notas son demasiado largas (máximo 500 caracteres).",
            ),
        ],
    )


class EditSessionForm(FlaskForm):
    """Form for editing an existing therapy session."""

    session_date = DateField(
        "Fecha", validators=[DataRequired(message="La fecha es requerida.")]
    )
    session_price = DecimalField(
        "Precio",
        places=2,
        validators=[
            DataRequired(message="El precio es requerido."),
            NumberRange(
                min=MIN_PRICE,
                max=MAX_PRICE,
                message=f"El precio debe estar entre ${MIN_PRICE} y ${MAX_PRICE:,.0f}.",
            ),
        ],
    )
    pending = BooleanField("Pago Pendiente")
    notes = TextAreaField(
        "Notas",
        validators=[
            Optional(),
            Length(max=500, message="Las notas son demasiado largas."),
        ],
    )


class TogglePaymentForm(FlaskForm):
    """Form for toggling session payment status (CSRF only)."""

    pass


class DeleteSessionForm(FlaskForm):
    """Form for deleting a session (CSRF only)."""

    pass


# =============================================================================
# Filter Forms
# =============================================================================


class FilterForm(FlaskForm):
    """Form for filtering sessions."""

    show = SelectField(
        "Mostrar",
        choices=[("all", "Todos"), ("pending", "Pendientes"), ("paid", "Pagados")],
        default="all",
    )

    class Meta:
        # Disable CSRF for GET requests (filter form)
        csrf = False


# =============================================================================
# Admin Forms
# =============================================================================


class UserForm(FlaskForm):
    """Form for creating/editing users (admin only)."""

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="El email es requerido."),
            Email(message="Ingresa un email válido."),
        ],
    )
    role = SelectField(
        "Rol",
        choices=[
            ("therapist", "Terapeuta"),
            ("admin", "Administrador"),
            ("viewer", "Solo Lectura"),
        ],
    )
    is_active = BooleanField("Activo", default=True)
