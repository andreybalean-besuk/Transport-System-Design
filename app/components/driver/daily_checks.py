import reflex as rx
from app.states.driver_state import DriverState


def form_section_header(title: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-5 h-5 text-[#0EA5E9]"),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800"),
        class_name="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100",
    )


def checkbox_item(
    label: str, checked: bool, on_change: rx.event.EventType
) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            checked=checked,
            on_change=on_change,
            class_name="w-5 h-5 rounded border-gray-300 text-[#0EA5E9] focus:ring-[#0EA5E9]",
        ),
        rx.el.span(label, class_name="text-gray-700 font-medium"),
        class_name="flex items-center gap-3 p-3 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer",
    )


def fluid_level_selector(
    label: str, current_value: str, fluid_type: str
) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm font-medium text-gray-600 mb-2"),
        rx.el.div(
            rx.foreach(
                ["OK", "Low", "Empty"],
                lambda level: rx.el.button(
                    level,
                    on_click=lambda: DriverState.set_fluid(fluid_type, level),
                    type="button",
                    class_name=rx.cond(
                        current_value == level,
                        "px-3 py-1.5 text-xs font-bold rounded-lg bg-[#0EA5E9] text-white shadow-md transition-all",
                        "px-3 py-1.5 text-xs font-medium rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-all",
                    ),
                ),
            ),
            class_name="flex gap-2",
        ),
        class_name="flex flex-col",
    )


def daily_checks_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Daily Vehicle Inspection", class_name="text-xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Complete pre-trip safety checks", class_name="text-sm text-gray-500"
            ),
            class_name="mb-6",
        ),
        form_section_header("Vehicle Information", "truck"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Vehicle ID",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.select(
                    rx.el.option(
                        "Select Vehicle", value="", disabled=True, selected=True
                    ),
                    rx.el.option("TRUCK-001", value="TRUCK-001"),
                    rx.el.option("TRUCK-002", value="TRUCK-002"),
                    rx.el.option("VAN-104", value="VAN-104"),
                    value=DriverState.vehicle_id,
                    on_change=DriverState.set_vehicle_id,
                    class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none",
                ),
                class_name="col-span-1",
            ),
            rx.el.div(
                rx.el.label(
                    "Odometer Reading",
                    class_name="block text-xs font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="number",
                    placeholder="e.g. 45000",
                    on_change=DriverState.set_odometer,
                    class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none",
                    default_value=DriverState.odometer,
                ),
                class_name="col-span-1",
            ),
            class_name="grid grid-cols-2 gap-4 mb-6",
        ),
        form_section_header("Safety Checklist", "clipboard-check"),
        rx.el.div(
            checkbox_item(
                "Lights & Indicators",
                DriverState.check_lights,
                lambda: DriverState.toggle_check("lights"),
            ),
            checkbox_item(
                "Tires & Wheels",
                DriverState.check_tires,
                lambda: DriverState.toggle_check("tires"),
            ),
            checkbox_item(
                "Brake System",
                DriverState.check_brakes,
                lambda: DriverState.toggle_check("brakes"),
            ),
            checkbox_item(
                "Mirrors",
                DriverState.check_mirrors,
                lambda: DriverState.toggle_check("mirrors"),
            ),
            checkbox_item(
                "Windshield",
                DriverState.check_windshield,
                lambda: DriverState.toggle_check("windshield"),
            ),
            checkbox_item(
                "Wipers & Washers",
                DriverState.check_wipers,
                lambda: DriverState.toggle_check("wipers"),
            ),
            checkbox_item(
                "Horn", DriverState.check_horn, lambda: DriverState.toggle_check("horn")
            ),
            checkbox_item(
                "Seatbelts",
                DriverState.check_seatbelts,
                lambda: DriverState.toggle_check("seatbelts"),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6",
        ),
        form_section_header("Fluids & Fuel", "droplets"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    f"Fuel Level: {DriverState.fuel_level}%",
                    class_name="block text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.input(
                    type="range",
                    min="0",
                    max="100",
                    default_value=DriverState.fuel_level,
                    key=DriverState.fuel_level.to_string(),
                    on_change=DriverState.set_fuel_level.throttle(500),
                    class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#0EA5E9]",
                ),
                class_name="mb-4 p-4 bg-gray-50 rounded-xl",
            ),
            rx.el.div(
                fluid_level_selector("Engine Oil", DriverState.fluid_oil, "oil"),
                fluid_level_selector("Coolant", DriverState.fluid_coolant, "coolant"),
                fluid_level_selector("Brake Fluid", DriverState.fluid_brake, "brake"),
                fluid_level_selector(
                    "Washer Fluid", DriverState.fluid_washer, "washer"
                ),
                class_name="grid grid-cols-2 gap-4",
            ),
            class_name="mb-6",
        ),
        form_section_header("Defects & Sign-off", "flag_triangle_right"),
        rx.el.div(
            rx.el.textarea(
                placeholder="Report any defects or issues found...",
                on_change=DriverState.set_defects,
                class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none min-h-[100px] mb-4",
                default_value=DriverState.defects,
            ),
            rx.el.input(
                placeholder="Driver Signature (Type Full Name)",
                on_change=DriverState.set_driver_signature,
                class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none mb-4",
                default_value=DriverState.driver_signature,
            ),
            rx.el.button(
                rx.icon("send", class_name="w-4 h-4 mr-2"),
                "Submit Daily Check",
                on_click=DriverState.submit_check,
                class_name="w-full py-3.5 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center",
            ),
            class_name="mb-2",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
    )


def check_history_item(check: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("check_check", class_name="w-5 h-5 text-green-500 mr-2"),
                rx.el.span(check["vehicle_id"], class_name="font-bold text-gray-800"),
                class_name="flex items-center",
            ),
            rx.el.span(
                check["timestamp"].split("T")[0], class_name="text-xs text-gray-500"
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.div(
            rx.el.span(
                f"Odometer: {check['odometer']}",
                class_name="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded mr-2",
            ),
            rx.el.span(
                f"Defects: {check['defects'] | 'None'}",
                class_name="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded",
            ),
            class_name="flex flex-wrap",
        ),
        class_name="p-4 border border-gray-100 rounded-xl hover:bg-gray-50 transition-colors",
    )


def daily_checks_history() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Recent Inspections", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.foreach(DriverState.checks, check_history_item),
            class_name="space-y-3 max-h-[400px] overflow-y-auto",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 h-full",
    )