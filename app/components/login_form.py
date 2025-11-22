import reflex as rx
from app.states.auth_state import AuthState


def role_selector() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name="role_selector",
                    checked=AuthState.role == "Driver",
                    on_change=lambda: AuthState.set_role("Driver"),
                    class_name="hidden peer",
                ),
                rx.el.div(
                    rx.icon("car-front", class_name="w-5 h-5 mb-1"),
                    rx.el.span("Driver"),
                    class_name="flex flex-col items-center justify-center w-full h-full text-gray-500 peer-checked:text-[#0EA5E9] transition-colors",
                ),
                class_name=rx.cond(
                    AuthState.role == "Driver",
                    "flex-1 cursor-pointer p-3 rounded-xl bg-[#0EA5E9]/10 border-2 border-[#0EA5E9] transition-all duration-200",
                    "flex-1 cursor-pointer p-3 rounded-xl border-2 border-transparent hover:bg-gray-50 transition-all duration-200",
                ),
            ),
            rx.el.label(
                rx.el.input(
                    type="radio",
                    name="role_selector",
                    checked=AuthState.role == "Manager",
                    on_change=lambda: AuthState.set_role("Manager"),
                    class_name="hidden peer",
                ),
                rx.el.div(
                    rx.icon("briefcase", class_name="w-5 h-5 mb-1"),
                    rx.el.span("Manager"),
                    class_name="flex flex-col items-center justify-center w-full h-full text-gray-500 peer-checked:text-[#0EA5E9] transition-colors",
                ),
                class_name=rx.cond(
                    AuthState.role == "Manager",
                    "flex-1 cursor-pointer p-3 rounded-xl bg-[#0EA5E9]/10 border-2 border-[#0EA5E9] transition-all duration-200",
                    "flex-1 cursor-pointer p-3 rounded-xl border-2 border-transparent hover:bg-gray-50 transition-all duration-200",
                ),
            ),
            class_name="flex gap-3 w-full mb-8 bg-white p-1",
        ),
        class_name="w-full",
    )


def login_input_field(
    label: str,
    placeholder: str,
    type_: str,
    value: str,
    on_change: rx.event.EventType,
    icon: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-medium text-gray-600 mb-1 ml-1 tracking-wider uppercase",
        ),
        rx.el.div(
            rx.icon(
                icon,
                class_name="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5",
            ),
            rx.el.input(
                type=type_,
                placeholder=placeholder,
                on_change=on_change,
                class_name="w-full pl-12 pr-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent transition-all duration-200 font-['JetBrains_Mono']",
                default_value=value,
            ),
            class_name="relative group",
        ),
        class_name="mb-5",
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("truck", class_name="w-8 h-8 text-white"),
                    class_name="w-12 h-12 rounded-xl bg-[#0EA5E9] flex items-center justify-center shadow-md mb-4",
                ),
                rx.el.h1(
                    "Transport Login",
                    class_name="text-2xl font-bold text-gray-900 tracking-tight",
                ),
                rx.el.p(
                    "Secure access for fleet personnel",
                    class_name="text-sm text-gray-500 mt-1",
                ),
                class_name="flex flex-col items-center text-center mb-8",
            ),
            rx.el.div(
                role_selector(),
                login_input_field(
                    "Email Address",
                    "user@transport.com",
                    "email",
                    AuthState.email,
                    AuthState.set_email,
                    "mail",
                ),
                login_input_field(
                    "Password",
                    "••••••••",
                    "password",
                    AuthState.password,
                    AuthState.set_password,
                    "lock",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.icon(
                            "circle-alert", class_name="w-4 h-4 mr-2 flex-shrink-0"
                        ),
                        rx.el.span(AuthState.error_message),
                        class_name="flex items-center p-3 mb-5 text-sm text-red-600 bg-red-50 rounded-lg border border-red-100 animate-pulse",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.el.div(
                            rx.el.div(
                                class_name="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"
                            ),
                            "Authenticating...",
                            class_name="flex items-center justify-center",
                        ),
                        rx.el.span(
                            "Sign In", class_name="flex items-center justify-center"
                        ),
                    ),
                    on_click=AuthState.login,
                    disabled=AuthState.is_loading,
                    class_name="w-full py-3.5 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-semibold rounded-xl shadow-md hover:shadow-lg transform transition-all duration-200 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center mt-2",
                ),
                class_name="w-full",
            ),
            class_name="bg-white p-8 rounded-[28px] shadow-xl border border-gray-100 w-full max-w-md relative overflow-hidden",
        ),
        class_name="flex flex-col items-center justify-center min-h-screen w-full p-4 bg-gray-50 font-['JetBrains_Mono']",
    )