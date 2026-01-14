"""
Authentication routes.

Handles login, logout, registration, and password reset.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import limiter
from app.services.auth_service import AuthService
from app.utils.constants import AUTH_RATE_LIMIT, FlashCategory
from app.validators.forms import (
    ChangePasswordForm,
    LoginForm,
    RegistrationForm,
    ResetPasswordForm,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit(AUTH_RATE_LIMIT)
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        success, user, message = AuthService.register(email=form.email.data, password=form.password.data)

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("auth.login"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit(AUTH_RATE_LIMIT)
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        success, user, message = AuthService.authenticate(email=form.email.data, password=form.password.data)

        if success:
            login_user(user, remember=form.remember_me.data)
            flash(message, FlashCategory.SUCCESS)

            # Redirect to next page or home
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("main.index"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout."""
    AuthService.logout(current_user)
    logout_user()
    flash("Sesión cerrada correctamente.", FlashCategory.SUCCESS)
    return redirect(url_for("auth.login"))


@auth_bp.route("/reset_password", methods=["GET", "POST"])
@limiter.limit(AUTH_RATE_LIMIT)
def reset_password():
    """Password reset page (legacy with security question)."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        success, message = AuthService.reset_password(
            email=form.email.data,
            new_password=form.new_password.data,
            security_answer=form.security.data,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("auth.login"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("auth/reset_password.html", form=form)


@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password for logged-in users."""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        success, message = AuthService.change_password(
            user=current_user,
            current_password=form.current_password.data,
            new_password=form.new_password.data,
        )

        if success:
            flash(message, FlashCategory.SUCCESS)
            return redirect(url_for("main.index"))
        else:
            flash(message, FlashCategory.ERROR)

    return render_template("auth/change_password.html", form=form)
