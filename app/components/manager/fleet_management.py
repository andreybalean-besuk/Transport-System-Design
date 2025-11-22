import reflex as rx
from app.states.manager_state import ManagerState


def vehicle_card(vehicle) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("truck", class_name="w-8 h-8 text-[#0EA5E9] mb-2"),
                rx.el.h3(vehicle.plate, class_name="font-bold text-gray-900 font-mono"),
                rx.el.p(
                    f"{vehicle.year} {vehicle.make} {vehicle.model}",
                    class_name="text-sm text-gray-600",
                ),
            ),
            rx.el.span(
                vehicle.status,
                class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full h-fit",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        class_name="p-4 border border-gray-100 rounded-xl bg-white hover:shadow-md transition-all",
    )


def fleet_management() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Fleet Management", class_name="text-xl font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.h3(
                    "Add New Vehicle",
                    class_name="text-sm font-bold text-gray-700 mb-3 uppercase",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Make (e.g. Ford)",
                        on_change=ManagerState.set_new_vehicle_make,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_vehicle_make,
                    ),
                    rx.el.input(
                        placeholder="Model (e.g. Transit)",
                        on_change=ManagerState.set_new_vehicle_model,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_vehicle_model,
                    ),
                    rx.el.input(
                        placeholder="Year",
                        on_change=ManagerState.set_new_vehicle_year,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_vehicle_year,
                    ),
                    rx.el.input(
                        placeholder="Plate Number",
                        on_change=ManagerState.set_new_vehicle_plate,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_vehicle_plate,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4 mr-2"),
                    "Add Vehicle",
                    on_click=ManagerState.add_vehicle,
                    class_name="w-full py-3 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md transition-all flex items-center justify-center mb-6",
                ),
                class_name="bg-gray-50 p-4 rounded-xl mb-6",
            ),
            rx.el.div(
                rx.cond(
                    ManagerState.vehicles.length() > 0,
                    rx.el.div(
                        rx.foreach(ManagerState.vehicles, vehicle_card),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                    ),
                    rx.el.p(
                        "No vehicles in fleet.",
                        class_name="text-gray-500 italic text-center py-8",
                    ),
                )
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="w-full animate-fadeIn",
    )