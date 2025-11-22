import reflex as rx
from app.states.manager_state import ManagerState


def driver_card(driver) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="w-6 h-6 text-white"),
                    class_name="w-10 h-10 rounded-full bg-[#0EA5E9] flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.h3(driver.name, class_name="font-bold text-gray-900"),
                    rx.el.p(driver.email, class_name="text-xs text-gray-500"),
                ),
            ),
            rx.el.span(
                driver.status,
                class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("License", class_name="text-xs text-gray-400 uppercase"),
                rx.el.p(
                    driver.license_number,
                    class_name="text-sm font-medium text-gray-700",
                ),
                class_name="mb-2",
            ),
            rx.el.div(
                rx.el.span("Phone", class_name="text-xs text-gray-400 uppercase"),
                rx.el.p(driver.phone, class_name="text-sm font-medium text-gray-700"),
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="p-4 border border-gray-100 rounded-xl bg-white hover:shadow-md transition-all",
    )


def driver_management() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Driver Management", class_name="text-xl font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.h3(
                    "Add New Driver",
                    class_name="text-sm font-bold text-gray-700 mb-3 uppercase",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Full Name",
                        on_change=ManagerState.set_new_driver_name,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_driver_name,
                    ),
                    rx.el.input(
                        placeholder="Email Address",
                        on_change=ManagerState.set_new_driver_email,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_driver_email,
                    ),
                    rx.el.input(
                        placeholder="Phone Number",
                        on_change=ManagerState.set_new_driver_phone,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_driver_phone,
                    ),
                    rx.el.input(
                        placeholder="License Number",
                        on_change=ManagerState.set_new_driver_license,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_driver_license,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Driver",
                    on_click=ManagerState.add_driver,
                    class_name="w-full py-3 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md transition-all flex items-center justify-center mb-6",
                ),
                class_name="bg-gray-50 p-4 rounded-xl mb-6",
            ),
            rx.el.div(
                rx.cond(
                    ManagerState.drivers.length() > 0,
                    rx.el.div(
                        rx.foreach(ManagerState.drivers, driver_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                    ),
                    rx.el.p(
                        "No drivers added yet.",
                        class_name="text-gray-500 italic text-center py-8",
                    ),
                )
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="w-full animate-fadeIn",
    )