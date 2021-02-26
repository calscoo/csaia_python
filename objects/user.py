from enums.role import roles


class user:
    def __init__(self, id, email, password, role):
        self._set_id(id)
        self._set_email(email)
        self._set_password(password)
        self._set_role(role)

    def _get_id(self):
        return self.id

    def _set_id(self, id):
        self.id = id

    def _get_email(self):
        return self.email

    def _set_email(self, email):
        self.email = email

    def _get_password(self):
        return self.password

    def _set_password(self, password):
        self.password = password

    def _get_role(self):
        return self.role

    def _set_role(self, role):
        if not isinstance(role, roles):
            raise TypeError("role must be of type enums.role")
        self.role = role

    def __str__(self):
        return \
            "user: { id: " + str(self.id) + ", " + \
            "email: " + str(self.email) + ", " + \
            "password: " + str(self.password) + ", " + \
            "role: " + str(self.role) + " }"
