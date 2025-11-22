import reflex as rx
from app.states.manager_state import ManagerState


def timesheets_overview() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Timesheets Approval", class_name="text-xl font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Clock In",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Clock Out",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Total Hours",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50 border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ManagerState.timesheets,
                            lambda ts: rx.el.tr(
                                rx.el.td(
                                    ts.date,
                                    class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50",
                                ),
                                rx.el.td(
                                    ts.clock_in.split("T")[1].split(".")[0],
                                    class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50 font-mono",
                                ),
                                rx.el.td(
                                    rx.cond(
                                        ts.clock_out,
                                        ts.clock_out.split("T")[1].split(".")[0],
                                        "--:--:--",
                                    ),
                                    class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50 font-mono",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        f"{ts.total_hours} hrs", class_name="font-bold"
                                    ),
                                    class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50",
                                ),
                                rx.el.td(
                                    rx.cond(
                                        ts.status == "Approved",
                                        rx.el.span(
                                            "Approved",
                                            class_name="px-2 py-1 text-xs font-bold text-green-700 bg-green-100 rounded-full",
                                        ),
                                        rx.cond(
                                            ts.status == "Rejected",
                                            rx.el.span(
                                                "Rejected",
                                                class_name="px-2 py-1 text-xs font-bold text-red-700 bg-red-100 rounded-full",
                                            ),
                                            rx.cond(
                                                ts.status == "Active",
                                                rx.el.span(
                                                    "Active",
                                                    class_name="px-2 py-1 text-xs font-bold text-blue-700 bg-blue-100 rounded-full",
                                                ),
                                                rx.el.span(
                                                    "Pending",
                                                    class_name="px-2 py-1 text-xs font-bold text-orange-700 bg-orange-100 rounded-full",
                                                ),
                                            ),
                                        ),
                                    ),
                                    class_name="py-3 px-4 text-sm border-b border-gray-50",
                                ),
                                rx.el.td(
                                    rx.cond(
                                        ts.status == "Completed",
                                        rx.el.div(
                                            rx.el.button(
                                                rx.icon("check", class_name="w-4 h-4"),
                                                on_click=lambda: ManagerState.approve_timesheet(
                                                    ts.id
                                                ),
                                                class_name="p-1.5 bg-green-100 text-green-600 rounded-lg hover:bg-green-200 transition-colors mr-2",
                                                title="Approve",
                                            ),
                                            rx.el.button(
                                                rx.icon("x", class_name="w-4 h-4"),
                                                on_click=lambda: ManagerState.reject_timesheet(
                                                    ts.id
                                                ),
                                                class_name="p-1.5 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors",
                                                title="Reject",
                                            ),
                                            class_name="flex items-center",
                                        ),
                                        rx.el.span("-", class_name="text-gray-400"),
                                    ),
                                    class_name="py-3 px-4 text-sm border-b border-gray-50",
                                ),
                                class_name="hover:bg-gray-50 transition-colors",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="w-full animate-fadeIn",
    )