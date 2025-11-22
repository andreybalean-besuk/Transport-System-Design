import reflex as rx
from app.states.auth_state import AuthState
from app.states.manager_state import ManagerState
from app.components.manager.overview import overview_table
from app.components.manager.timesheets_overview import timesheets_overview
from app.components.manager.driver_management import driver_management
from app.components.manager.fleet_management import fleet_management
from app.components.manager.maintenance import maintenance
from app.components.manager.messaging import messaging
from app.components.pwa.sync_indicator import sync_indicator
from app.states.sync_state import SyncState


def nav_item(label: str, icon: str, tab_id: str) -> rx.Component:
    active = ManagerState.current_tab == tab_id
    return rx.el.button(
        rx.icon(
            icon,
            class_name=rx.cond(
                active, "w-5 h-5 text-[#0EA5E9]", "w-5 h-5 text-gray-500"
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                active,
                "ml-3 font-bold text-[#0EA5E9]",
                "ml-3 font-medium text-gray-500",
            ),
        ),
        on_click=lambda: ManagerState.set_current_tab(tab_id),
        class_name=rx.cond(
            active,
            "flex items-center w-full px-4 py-3 bg-[#0EA5E9]/10 rounded-xl mb-1 transition-colors",
            "flex items-center w-full px-4 py-3 hover:bg-gray-100 rounded-xl mb-1 transition-colors",
        ),
    )


def manager_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Manager", class_name="text-xl font-bold text-gray-900"),
            rx.el.button(
                rx.icon("log-out", class_name="w-5 h-5"),
                on_click=AuthState.logout,
                class_name="p-2 text-red-600 bg-red-50 rounded-lg",
            ),
            class_name="md:hidden flex justify-between items-center p-4 bg-white border-b border-gray-200 sticky top-0 z-50",
        ),
        rx.el.div(
            rx.el.aside(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "shield-check", class_name="w-8 h-8 text-[#0EA5E9] mb-2"
                        ),
                        rx.el.h1(
                            "Manager", class_name="text-xl font-bold text-gray-900"
                        ),
                        rx.el.div(sync_indicator(), class_name="mt-2"),
                        class_name="p-6 mb-4",
                    ),
                    rx.el.nav(
                        nav_item("Overview", "layout-dashboard", "overview"),
                        nav_item("Timesheets", "clock", "timesheets"),
                        nav_item("Drivers", "users", "drivers"),
                        nav_item("Fleet", "truck", "fleet"),
                        nav_item("Maintenance", "wrench", "maintenance"),
                        nav_item("Messaging", "message-square", "messaging"),
                        class_name="px-4",
                    ),
                    class_name="flex-1 overflow-y-auto",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("log-out", class_name="w-5 h-5 mr-3"),
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="flex items-center w-full px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl font-medium transition-colors",
                    ),
                    class_name="p-4 border-t border-gray-100",
                ),
                class_name="hidden md:flex flex-col w-64 bg-white border-r border-gray-200 h-screen sticky top-0",
            ),
            rx.el.main(
                rx.el.div(
                    rx.el.div(
                        rx.el.button(
                            "Overview",
                            on_click=lambda: ManagerState.set_current_tab("overview"),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        rx.el.button(
                            "Timesheets",
                            on_click=lambda: ManagerState.set_current_tab("timesheets"),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        rx.el.button(
                            "Drivers",
                            on_click=lambda: ManagerState.set_current_tab("drivers"),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        rx.el.button(
                            "Fleet",
                            on_click=lambda: ManagerState.set_current_tab("fleet"),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        rx.el.button(
                            "Maintenance",
                            on_click=lambda: ManagerState.set_current_tab(
                                "maintenance"
                            ),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        rx.el.button(
                            "Messaging",
                            on_click=lambda: ManagerState.set_current_tab("messaging"),
                            class_name="whitespace-nowrap px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-full border border-gray-200",
                        ),
                        class_name="md:hidden flex gap-2 overflow-x-auto p-4 bg-gray-50 no-scrollbar",
                    ),
                    rx.el.div(
                        rx.cond(
                            ManagerState.current_tab == "overview", overview_table()
                        ),
                        rx.cond(
                            ManagerState.current_tab == "timesheets",
                            timesheets_overview(),
                        ),
                        rx.cond(
                            ManagerState.current_tab == "drivers", driver_management()
                        ),
                        rx.cond(
                            ManagerState.current_tab == "fleet", fleet_management()
                        ),
                        rx.cond(
                            ManagerState.current_tab == "maintenance", maintenance()
                        ),
                        rx.cond(ManagerState.current_tab == "messaging", messaging()),
                        class_name="p-4 md:p-8 max-w-7xl mx-auto",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex-1 bg-gray-50 min-h-screen",
            ),
            class_name="flex flex-col md:flex-row w-full min-h-screen font-['JetBrains_Mono']",
        ),
        on_mount=[
            AuthState.check_login,
            ManagerState.on_load,
            SyncState.check_pending_count,
        ],
    )