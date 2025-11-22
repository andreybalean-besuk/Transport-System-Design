import reflex as rx
from app.states.manager_state import ManagerState


def maintenance_item(record) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("wrench", class_name="w-5 h-5 text-orange-500 mr-3 mt-1"),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        record.vehicle_id, class_name="font-bold text-gray-800 mr-2"
                    ),
                    rx.el.span(
                        record.type,
                        class_name="text-sm bg-gray-100 px-2 py-0.5 rounded text-gray-600",
                    ),
                    class_name="flex items-center mb-1",
                ),
                rx.el.p(record.description, class_name="text-sm text-gray-600"),
                class_name="flex-1",
            ),
            class_name="flex items-start",
        ),
        rx.el.div(
            rx.el.span(
                record.scheduled_date, class_name="text-sm font-medium text-gray-700"
            ),
            rx.el.span(
                record.status,
                class_name="text-xs text-orange-600 bg-orange-50 px-2 py-1 rounded-full ml-2",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name="flex justify-between items-start p-4 border-b border-gray-100 last:border-0",
    )


def maintenance() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Maintenance Schedule",
                class_name="text-xl font-bold text-gray-900 mb-4",
            ),
            rx.el.div(
                rx.el.h3(
                    "Schedule Service",
                    class_name="text-sm font-bold text-gray-700 mb-3 uppercase",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Select Vehicle", value="", disabled=True, selected=True
                        ),
                        rx.foreach(
                            ManagerState.vehicles,
                            lambda v: rx.el.option(v.plate, value=v.plate),
                        ),
                        on_change=ManagerState.set_new_maint_vehicle_id,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none bg-white",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Service Type", value="", disabled=True, selected=True
                        ),
                        rx.el.option("Routine Service", value="Routine Service"),
                        rx.el.option("Tire Change", value="Tire Change"),
                        rx.el.option("Repair", value="Repair"),
                        rx.el.option("Inspection", value="Inspection"),
                        on_change=ManagerState.set_new_maint_type,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none bg-white",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=ManagerState.set_new_maint_date,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                    ),
                    rx.el.input(
                        placeholder="Description",
                        on_change=ManagerState.set_new_maint_desc,
                        class_name="p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none",
                        default_value=ManagerState.new_maint_desc,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                ),
                rx.el.button(
                    rx.icon("calendar-plus", class_name="w-4 h-4 mr-2"),
                    "Schedule Maintenance",
                    on_click=ManagerState.schedule_maintenance,
                    class_name="w-full py-3 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md transition-all flex items-center justify-center mb-6",
                ),
                class_name="bg-gray-50 p-4 rounded-xl mb-6",
            ),
            rx.el.div(
                rx.cond(
                    ManagerState.maintenance.length() > 0,
                    rx.el.div(
                        rx.foreach(ManagerState.maintenance, maintenance_item),
                        class_name="border border-gray-200 rounded-xl overflow-hidden",
                    ),
                    rx.el.p(
                        "No maintenance scheduled.",
                        class_name="text-gray-500 italic text-center py-8",
                    ),
                )
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="w-full animate-fadeIn",
    )