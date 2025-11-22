import reflex as rx
from app.states.sync_state import SyncState


def install_banner() -> rx.Component:
    return rx.cond(
        SyncState.show_install_banner,
        rx.el.div(
            rx.el.div(
                rx.icon("download", class_name="w-5 h-5 text-[#0EA5E9] mr-3"),
                rx.el.div(
                    rx.el.p(
                        "Install App", class_name="font-bold text-sm text-gray-900"
                    ),
                    rx.el.p(
                        "Add to home screen for offline access",
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center flex-1",
            ),
            rx.el.button(
                rx.icon("x", class_name="w-4 h-4 text-gray-400"),
                on_click=SyncState.close_install_banner,
                class_name="p-2 hover:bg-gray-100 rounded-full",
            ),
            class_name="mx-4 mb-4 p-3 bg-white rounded-xl shadow-md border border-gray-100 flex items-center justify-between animate-slideUp",
        ),
    )