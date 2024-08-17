import json
from flask import Blueprint, jsonify

from src.controllers.auth import login, confirm_email, refresh_token, resend_token, handle_google_signin, update_password
from src.utils.decorators import token_required
from src.utils.token import confirm_token
from src.controllers.user import add_user, request, request_password_reset


auth = Blueprint("auth", __name__)
base_url = "/api/auth"


@auth.route(f"{base_url}/register", methods=["POST"])
def create():
    response, status = add_user()

    if status == 201:
        email = response.json.get("data").get("email")
        response, status = login(
            {"email": email, "password": request.json.get("password")}
        )
        data = response.json
        data.update(
            {
                "message": "User registered successfully. Please check your email to confirm your account."
            }
        )
        response.data = json.dumps(data)
        print(response.json)
        return response
    return response, status

@auth.route(f"{base_url}/google-signin", methods=["POST"])
def google_signin():
    print(request.json)
    response, status = handle_google_signin(request.json)
    return response, status


@auth.route(f"{base_url}/login", methods=["POST"])
def handle_login():
    response = login()
    return response


@auth.route(f"{base_url}/confirm/<token>", methods=["GET"])
@token_required
def confirm(current_user: dict, token: str):
    response = confirm_email(current_user, token)
    return response


@auth.route(f"{base_url}/confirm/resend", methods=["GET"])
@token_required
def resend_confirmation(current_user: dict):
    response = resend_token(current_user)
    return response


@auth.route(f"{base_url}/refresh", methods=["GET"])
def refresh():
    response = refresh_token()
    return response

@auth.route(f"{base_url}/forgot_password", methods=["POST"])
def forgot_password():
    
    response, status = request_password_reset()

    if status == 200:    
        data = response.json
        data.update(
            {
                "message": "Password reset email sent successfully. Please check your email to reset your password."
            }
        )
        response.data = json.dumps(data)
        return response

    return response, status 


@auth.route(f"{base_url}/reset-password", methods=['POST'])
def reset_password(token):
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400
    
    email = confirm_token(token)
    
    if not email:
        return jsonify({"message": "Invalid or expired token", "error": "Token verification failed"}), 400
    
    if update_password(email, new_password):
        return jsonify({"message": "Password has been reset successfully"}), 200
    else:
        return jsonify({"message": "Failed to reset password", "error": "User not found"}), 500

