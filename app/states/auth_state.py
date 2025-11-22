import reflex as rx
import asyncio
import re


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    role: str = "Driver"
    is_loading: bool = False
    error_message: str = ""
    session_token: str = ""
    _dashboard_routes: dict[str, str] = {
        "Driver": "/driver-dashboard",
        "Manager": "/manager-dashboard",
    }

    @rx.event
    def set_role(self, role: str):
        self.role = role

    @rx.event
    def set_email(self, email: str):
        self.email = email
        self.error_message = ""

    @rx.event
    def set_password(self, password: str):
        self.password = password
        self.error_message = ""

    @rx.event
    def validate_inputs(self) -> bool:
        if not self.email or not self.password:
            self.error_message = "Please fill in all fields."
            return False
        email_pattern = "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
        if not re.match(email_pattern, self.email):
            self.error_message = "Please enter a valid email address."
            return False
        if len(self.password) < 6:
            self.error_message = "Password must be at least 6 characters."
            return False
        return True

    @rx.event
    async def login(self):
        self.is_loading = True
        self.error_message = ""
        yield
        await asyncio.sleep(1.5)
        if not self.validate_inputs():
            self.is_loading = False
            yield
            return
        if self.password == "password123":
            import secrets

            self.session_token = secrets.token_hex(16)
            self.is_loading = False
            target_route = self._dashboard_routes.get(self.role, "/")
            yield rx.redirect(target_route)
        else:
            self.error_message = "Invalid credentials. Try 'password123'."
            self.is_loading = False

    @rx.event
    def logout(self):
        self.session_token = ""
        self.email = ""
        self.password = ""
        self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def check_login(self):
        """Called on_load by protected pages"""
        if not self.session_token:
            return rx.redirect("/")