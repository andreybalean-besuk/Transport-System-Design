import reflex as rx
from app.states.auth_state import AuthState
from app.states.driver_state import DriverState
from app.components.driver.daily_checks import daily_checks_form, daily_checks_history
from app.components.driver.timesheets import timesheet_card
from app.components.driver.messages import messages_card
from app.components.pwa.sync_indicator import sync_indicator
from app.components.pwa.install_banner import install_banner
from app.states.sync_state import SyncState


def tab_button(label: str, icon: str, tab_value: str) -> rx.Component:
    active = DriverState.current_tab == tab_value
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(
                active, "w-5 h-5 text-white mb-1", "w-5 h-5 text-gray-500 mb-1"
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                active,
                "text-xs font-bold text-white",
                "text-xs font-medium text-gray-500",
            ),
        ),
        on_click=lambda: DriverState.set_current_tab(tab_value),
        class_name=rx.cond(
            active,
            "flex flex-col items-center justify-center p-3 rounded-xl bg-[#0EA5E9] shadow-md transition-all w-full",
            "flex flex-col items-center justify-center p-3 rounded-xl bg-white hover:bg-gray-50 border border-gray-200 transition-all w-full",
        ),
    )


def driver_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                tab_button("Checks", "clipboard-check", "checks"),
                tab_button("Timesheet", "clock", "timesheets"),
                tab_button("Messages", "message-square", "messages"),
                class_name="grid grid-cols-3 gap-4 w-full max-w-md mx-auto",
            ),
            class_name="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 p-4 z-50 md:hidden safe-area-pb",
        ),
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Driver Dashboard",
                            class_name="text-2xl font-bold text-gray-900",
                        )
                    ),
                    rx.el.div(
                        sync_indicator(),
                        rx.el.button(
                            rx.icon("log-out", class_name="w-5 h-5 ml-3 mr-2"),
                            "Logout",
                            on_click=AuthState.logout,
                            class_name="flex items-center px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-start mb-8",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                tab_button("Daily Checks", "clipboard-check", "checks"),
                tab_button("Timesheets", "clock", "timesheets"),
                tab_button("Messages", "message-square", "messages"),
                class_name="hidden md:grid grid-cols-3 gap-4 mb-8 max-w-lg",
            ),
            rx.el.div(
                rx.cond(
                    DriverState.current_tab == "checks",
                    rx.el.div(
                        rx.el.div(daily_checks_form(), class_name="lg:col-span-2"),
                        rx.el.div(daily_checks_history(), class_name="lg:col-span-1"),
                        class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 pb-24 md:pb-0",
                    ),
                ),
                rx.cond(
                    DriverState.current_tab == "timesheets",
                    rx.el.div(
                        timesheet_card(), class_name="max-w-2xl mx-auto pb-24 md:pb-0"
                    ),
                ),
                rx.cond(
                    DriverState.current_tab == "messages",
                    rx.el.div(
                        messages_card(), class_name="max-w-2xl mx-auto pb-24 md:pb-0"
                    ),
                ),
                class_name="w-full animate-fadeIn",
            ),
            install_banner(),
            class_name="flex flex-col p-6 min-h-screen bg-gray-50 font-['JetBrains_Mono'] max-w-7xl mx-auto w-full",
        ),
        on_mount=[
            AuthState.check_login,
            DriverState.on_load,
            SyncState.check_pending_count,
        ],
    )