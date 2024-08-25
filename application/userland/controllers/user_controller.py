from flask import request
from application.userland.controller import mod_userland
from application.core.utils.user_utils import UserUtils


@mod_userland.route('/user', methods=['POST'])
def sign_up():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')
    response = UserUtils.user_register(name, surname, email, password)
    return response


@mod_userland.route('/signin', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')
    response = UserUtils.user_controller(email, password)
    return response


@mod_userland.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    password = request.form.get('password')
    response = UserUtils.reset_password(email, password)
    return response


@mod_userland.route('/getresponse', methods=['POST'])
def get_response():
    text = request.form.get('input')
    keywords = request.form.get('keywords').split(",")
    response_gemini = UserUtils.process_gemini(text, keywords)
    response_openai = UserUtils.process_openai(text, keywords)
    response_edenai = UserUtils.process_eden_ai(text, keywords)
    print("openai: ", response_openai[text], "\n gemini: ", response_gemini[text], "\n edenai: ", response_edenai[text])
    if response_gemini[text] >= response_edenai[text] and response_gemini[text] >= response_openai[text]:
        return response_gemini
    elif response_openai[text] >= response_gemini[text] and response_openai[text] > response_edenai[text]:
        return response_openai
    else:
        return response_edenai
