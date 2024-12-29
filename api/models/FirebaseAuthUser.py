class FirebaseAuthUser:
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email
        }

    @property
    def is_authenticated(self):
        return True  # Since the token is valid, consider the user authenticated

    @property
    def is_active(self):
        return True  # Assuming all Firebase users are active by default
