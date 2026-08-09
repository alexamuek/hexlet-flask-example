from flask import session


class Repository:

	def get_content(self):
		return session.get("users_list", [])

	def find(self, id):
		users = session.get("users_list", [])
		user = next(item for item in users if item["id"] == id)
		return user

	def save(self, user):
	        if "id" in user and user["id"]:
	            self._update(user)
	        else:
	            self._create(user)

	def _create(self, user):
	    session.setdefault("users_list", [])
	    next_id = max([item["id"] for item in  session["users_list"]], default=0) + 1
	    session["users_list"].append({**user,**{"id": next_id}})


	def _update(self, user):
	    users = session.get("users_list", [])
	    new_users = []
	    for item in users:
	        if item["id"] == user["id"]:
	            new_users.append(user)
	        else:
	            new_users.append(item)
	    session["users_list"] = new_users

	def delete(self, user_id):
		users = session.get("users_list", None)
		new_list = list(user for user in users if user["id"] != user_id)
		session["users_list"] = new_list
        