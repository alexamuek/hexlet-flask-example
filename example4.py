from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json
import repository2
import psycopg2
from dotenv import load_dotenv  # Импортируем dotenv
import os


conn = psycopg2.connect(
    dbname=os.getenv("DBNAME"), user=os.getenv("USER"), password=os.getenv("PASSwORD"), host=os.getenv("HOST"), port=os.getenv("PORT"))
repo = repository2.Repository(conn)


# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
app.logger.setLevel("INFO")
load_dotenv()  # Загрузка переменных окружения из файла .env


@app.get("/users")
def users_index():
    users = repo.get_content()
    app.logger.info(f"here!! {users}")
    return render_template(
            "users/index3.html",
            users=users
        )

@app.get("/users/<int:id>")
def users_show(id):
    user=repo.find(id)
    return render_template(
            "users/show1.html",
            user=user
        )


@app.route("/users/new")
def users_new():
    user = {
        "name": "",
        "email": ""
    }
    errors = {}

    return render_template("users/new.html", user=user, errors=errors)

@app.post("/users")
def users_post():
    # извлекаем данные из формы
    user = request.form.to_dict()
    app.logger.info(user)
    # валидируем данные
    errors = validate(user)
    if errors:
        flash("Bad data!!", "error")
        return render_template(
            "users/new.html",
            user=user,
            errors=errors,
        ), 422
    # сохраняем нового пользователя
    repo.save(user)
    flash("User was added!", "success")
    # делаем редирект на список пользователей
    return redirect(url_for('users_index'), code=302)

@app.route("/users/<int:id>/delete", methods=["POST"])
def users_delete(id):
    repo.delete(id)
    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))

@app.route("/users/<int:id>/edit")
def users_edit(id):
    user = repo.find(id)
    errors = []
    return render_template(
        "users/edit.html",
        user=user,
        errors=errors,
    )

@app.route("/users/<int:id>/patch", methods=["POST"])
def users_patch(id):
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            "users/edit.html",
            user=data,
            errors=errors,
        ), 422
    repo.save({**data, **{"id": int(id)}})
    flash("User has been updated", "success")
    return redirect(url_for("users_index"))

def validate(data):
    errors = {}
    if len(data["name"]) < 3:
        errors["name"] = "Bad name!"
    if len(data["email"]) < 10:
        errors["email"] = "Bad email format!"
    return errors



# uv run flask --app example4 run --port 8000  - запуск development сервера