import reflex as rx
from app.states.driver_state import DriverState


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "Active",
            "px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-bold uppercase tracking-wider",
            "px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-xs font-bold uppercase tracking-wider",
        ),
    )


def timesheet_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Timesheet Actions", class_name="text-xl font-bold text-gray-900"),
            rx.el.p("Track your shift hours", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("clock", class_name="w-8 h-8 mb-2"),
                rx.el.span("Clock In", class_name="font-bold"),
                on_click=DriverState.clock_in,
                class_name="flex flex-col items-center justify-center p-6 rounded-2xl bg-[#0EA5E9] text-white shadow-lg hover:shadow-xl hover:bg-[#0284C7] transition-all active:scale-95",
            ),
            rx.el.button(
                rx.icon("coffee", class_name="w-8 h-8 mb-2"),
                rx.el.span("Start Break", class_name="font-bold"),
                on_click=DriverState.start_break,
                class_name="flex flex-col items-center justify-center p-6 rounded-2xl bg-orange-500 text-white shadow-lg hover:shadow-xl hover:bg-orange-600 transition-all active:scale-95",
            ),
            rx.el.button(
                rx.icon("circle_play", class_name="w-8 h-8 mb-2"),
                rx.el.span("End Break", class_name="font-bold"),
                on_click=DriverState.end_break,
                class_name="flex flex-col items-center justify-center p-6 rounded-2xl bg-green-500 text-white shadow-lg hover:shadow-xl hover:bg-green-600 transition-all active:scale-95",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="w-8 h-8 mb-2"),
                rx.el.span("Clock Out", class_name="font-bold"),
                on_click=DriverState.clock_out,
                class_name="flex flex-col items-center justify-center p-6 rounded-2xl bg-gray-800 text-white shadow-lg hover:shadow-xl hover:bg-gray-900 transition-all active:scale-95",
            ),
            class_name="grid grid-cols-2 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Today's Shift", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            rx.cond(
                DriverState.timesheets.length() > 0,
                rx.el.div(
                    rx.foreach(
                        DriverState.timesheets,
                        lambda ts: rx.cond(
                            ts.status == "Active",
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "Status",
                                        class_name="text-xs text-gray-500 uppercase",
                                    ),
                                    status_badge(ts.status),
                                    class_name="flex justify-between items-center mb-2",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Clocked In",
                                        class_name="text-xs text-gray-500 uppercase",
                                    ),
                                    rx.el.span(
                                        ts.clock_in.split("T")[1].split(".")[0],
                                        class_name="font-mono font-medium text-gray-800",
                                    ),
                                    class_name="flex justify-between items-center mb-2",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        "Breaks Taken",
                                        class_name="text-xs text-gray-500 uppercase",
                                    ),
                                    rx.el.span(
                                        ts.breaks.length(),
                                        class_name="font-mono font-medium text-gray-800",
                                    ),
                                    class_name="flex justify-between items-center",
                                ),
                                class_name="p-4 bg-blue-50 border border-blue-100 rounded-xl",
                            ),
                            rx.fragment(),
                        ),
                    )
                ),
                rx.el.div(
                    "No active shift. Please clock in.",
                    class_name="p-4 bg-gray-50 text-gray-500 rounded-xl text-center italic",
                ),
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Recent Timesheets",
                class_name="text-lg font-semibold text-gray-800 mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    DriverState.timesheets,
                    lambda ts: rx.el.div(
                        rx.el.div(
                            rx.el.span(ts.date, class_name="font-bold text-gray-800"),
                            rx.el.span(
                                f"{ts.total_hours} hrs",
                                class_name="font-mono font-bold text-[#0EA5E9]",
                            ),
                            class_name="flex justify-between items-center mb-1",
                        ),
                        rx.el.div(
                            rx.el.span(
                                f"In: {ts.clock_in.split('T')[1].split('.')[0]}",
                                class_name="text-xs text-gray-500",
                            ),
                            rx.cond(
                                ts.clock_out,
                                rx.el.span(
                                    f"Out: {ts.clock_out.split('T')[1].split('.')[0]}",
                                    class_name="text-xs text-gray-500",
                                ),
                                rx.el.span(
                                    "Active",
                                    class_name="text-xs text-green-500 font-medium",
                                ),
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        class_name="p-3 border border-gray-100 rounded-xl hover:bg-gray-50 transition-colors",
                    ),
                ),
                class_name="space-y-3 max-h-[300px] overflow-y-auto",
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="flex flex-col gap-4",
    )