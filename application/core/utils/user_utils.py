import os
import google.generativeai as genai
import openai
import requests
from flask import jsonify
from flask import current_app
from application.core.db_models import Users
from application import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserUtils:
    @staticmethod
    def user_register(name, surname, email, password):
        response = {}
        already_have_user = Users.query.filter(Users.email == email).first()
        if not already_have_user:
            if email and password:
                user = Users(
                    name=name,
                    surname=surname,
                    email=email,
                    password=password
                )
                db.session.add(user)
                db.session.commit()
        else:
            response = {}
        return response

    @staticmethod
    def user_controller(email, password):
        response = {}
        user = Users.query.filter(Users.email == email).first()
        if user:
            if user.password == password:
                response["message"] = "Login successful."
            else:
                response["message"] = "Invalid password."
        else:
            response["message"] = "User not found."
        return response

    @staticmethod
    def reset_password(email, password):
        response = {}
        user = Users.query.filter(Users.email == email).first()
        if user:
            user.password = password
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'fail'
        return response

    @staticmethod
    def process_gemini(input, keywords):
        res = {}
        count = 0
        os.environ['GOOGLE_API_KEY'] = "AIzaSyAsF5zw1XmScM2ixjihC3d_ZpIecY-ewow"
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        generation_config = {"temperature":0, "max_tokens":400, "top_p":1, "top_k":1}
        safety_settings = [{"category":"HARM_CATEGORY_HARASSMENT", "threshold":"BLOCK_NONE"},
                           {"category":"HARM_CATEGORY_HATE_SPEECH", "threshold":"BLOCK_NONE"},
                           {"category":"HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold":"BLOCK_NONE"},
                           {"category":"HARM_CATEGORY_DANGEROUS_CONTENT", "threshold":"BLOCK_NONE"}]
        model = genai.GenerativeModel('gemini-pro')
        headers = {'Accept': 'application/json'}

        response = model.generate_content(input, safety_settings=safety_settings)

        output_text = response.text.lower().replace("*","")
        for keyword in keywords:
            if keyword.lower() in output_text:
                count += 1
        res['text'] = output_text
        res['name'] = 'gemini'
        res[input] = count
        return res

    @staticmethod
    def process_eden_ai(input,keywords):
        res = {}
        url = "https://api.edenai.run/v2/text/chat"
        count = 0
        payload = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "temperature": 0,
            "max_tokens": 1000,
            "providers": ["openai"],
            "text": input
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZWNmMTU2NGEtYTJjNi00MmY1LTgyZjUtZjBlNjE1OTIzZGMzIiwidHlwZSI6ImFwaV90b2tlbiJ9.XuSohPKg6VlDwFXlF0VN80SZDJA7_gfQ50YbR72ZePA"
        }

        response = requests.post(url, json=payload, headers=headers)
        output_text = response.json()['openai']['generated_text']
        for keyword in keywords:
            if keyword.lower() in output_text.lower():
                count += 1

        res['text'] = output_text
        res['name'] = 'edenai'
        res[input] = count
        return res

    @staticmethod
    def process_openai(input, keywords):
        res = {}
        count = 0
        client = openai.OpenAI(api_key='sk-proj-Ii8EHsjghYllQspbrFzVT3BlbkFJrxasTR1rr2TIhJvHzazQ')

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": input}
            ]
        )
        output_text = completion.choices[0].message.content
        for keyword in keywords:
            if keyword.lower() in output_text.lower():
                count += 1

        res['text'] = output_text
        res['name'] = 'openai'
        res[input] = count
        return res


