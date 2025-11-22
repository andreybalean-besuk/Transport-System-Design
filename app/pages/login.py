import reflex as rx
from app.components.login_form import login_form


def login_page() -> rx.Component:
    return rx.el.div(
        login_form(),
        rx.el.div(
            class_name="fixed top-0 left-0 w-full h-64 bg-[#0EA5E9]/5 -z-10 rounded-b-[50px]"
        ),
        rx.el.div(
            class_name="fixed bottom-0 right-0 w-64 h-64 bg-[#0EA5E9]/5 -z-10 rounded-tl-[100px]"
        ),
        class_name="relative w-full h-full",
    )