import reflex as rx
from app.states.manager_state import ManagerState


def overview_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Daily Checks Overview",
                class_name="text-xl font-bold text-gray-900 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search by Vehicle ID or Driver...",
                        on_change=ManagerState.set_overview_search.debounce(500),
                        class_name="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none",
                    ),
                    class_name="relative max-w-md mb-6",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Vehicle",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Odometer",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Defects",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="text-left py-3 px-4 text-xs font-semibold text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50 border-b border-gray-100",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ManagerState.checks,
                            lambda check: rx.cond(
                                (ManagerState.overview_search == "")
                                | check.vehicle_id.lower().contains(
                                    ManagerState.overview_search.lower()
                                ),
                                rx.el.tr(
                                    rx.el.td(
                                        check.timestamp.split("T")[0],
                                        class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            check.vehicle_id,
                                            class_name="font-mono font-medium",
                                        ),
                                        class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50",
                                    ),
                                    rx.el.td(
                                        check.odometer,
                                        class_name="py-3 px-4 text-sm text-gray-700 border-b border-gray-50",
                                    ),
                                    rx.el.td(
                                        rx.cond(
                                            check.defects.length() > 0,
                                            rx.el.span(
                                                check.defects,
                                                class_name="text-red-600 text-xs font-medium px-2 py-1 bg-red-50 rounded-lg",
                                            ),
                                            rx.el.span(
                                                "None",
                                                class_name="text-green-600 text-xs font-medium px-2 py-1 bg-green-50 rounded-lg",
                                            ),
                                        ),
                                        class_name="py-3 px-4 text-sm border-b border-gray-50",
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            "Submitted",
                                            class_name="text-xs font-bold text-blue-600",
                                        ),
                                        class_name="py-3 px-4 text-sm border-b border-gray-50",
                                    ),
                                    class_name="hover:bg-gray-50 transition-colors",
                                ),
                                rx.fragment(),
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