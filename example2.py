from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json

# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = "Alex_secret_key"
file = 'data.json'
app.logger.setLevel("INFO")


@app.get("/users")
def users_index():
    users = get_data()
    app.logger.info(users)
    return render_template(
            "users/index3.html",
            users=users
        )

@app.get("/users/<int:id>")
def users_show(id):
    users = get_data()
    app.logger.info(users)
    user = next(item for item in users if item["id"] == id)
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
    save(user)
    flash("User was added!", "success")
    # делаем редирект на список пользователей
    return redirect(url_for('users_index'), code=302)

@app.route("/users/<int:id>/edit")
def users_edit(id):
    user = find_user(id)
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
            user=user,
            errors=errors,
        ), 422

    update(data, id)
    flash("User has been updated", "success")
    return redirect(url_for("users_index"))

@app.route("/users/<id>/delete", methods=["POST"])
def users_delete(id):
    destroy(id)
    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))


def save(data):
    with open(file, 'a') as f:
        existing = get_data()
        new_id = max([item["id"] for item in existing], default=0) + 1
        before_json = {"id": new_id, "name": data["name"], "email": data["email"]}
        json_data = json.dumps(before_json)
        f.write(json_data+'\n')

def get_data():
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
        lines = data.split('\n')
        result = [json.loads(line) for line in lines if line.strip()]
    return result

def validate(data):
    errors = {}
    if len(data["name"]) < 3:
        errors["name"] = "Bad name!"
    if len(data["email"]) < 10:
        errors["email"] = "Bad email format!"
    return errors

def update(user, user_id):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    lines = data.split('\n')
    new_lines = []
    for item in lines:
        if not item.strip():           # если пустая
            continue 
        if json.loads(item)["id"] == user_id:
            new_lines.append(json.dumps({"id": user_id, "name": user["name"], "email": user["email"]}))
        else:
            new_lines.append(item)
    data_to_save = "\n".join(new_lines)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data_to_save)

def find_user(id):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
        lines = data.split('\n')
        result = next(json.loads(line) for line in lines if json.loads(line)["id"] == id)
    return result


def destroy(user_id):
    app.logger.info(f"=== DELETE USER {user_id} ===")  # ← ЭТО
    
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    lines = data.split('\n')
    new_lines = []
    for item in lines:
        if not item.strip():
            continue 
        parsed = json.loads(item)
        if parsed["id"] != int(user_id):
            new_lines.append(json.dumps({"id": parsed["id"], "name": parsed["name"], "email": parsed["email"]}))
        app.logger.info(f"new_lines after {new_lines}")
    
    app.logger.info(f"NEW LINES COUNT: {len(new_lines)}")  # ← И ЭТО
    
    data_to_save = "\n".join(new_lines)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data_to_save)

# uv run flask --app example run --port 8000  - запуск development сервера