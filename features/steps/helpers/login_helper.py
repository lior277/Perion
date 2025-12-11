class LoginHelper:

    def login_user(self, context, username: str, password: str):
        """General login method used internally."""
        context.pages.login.open()
        context.pages.login.login(username, password)

    def login(self, context, user_type: str):
        """Used for scenario outline login."""
        user_type = user_type.lower()
        if user_type not in context.users:
            raise ValueError(f"Unknown user type: {user_type}")

        user = context.users[user_type]
        self.login_user(context, user["username"], user["password"])
