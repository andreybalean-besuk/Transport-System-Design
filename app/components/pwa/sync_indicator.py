import reflex as rx
from app.states.sync_state import SyncState


def sync_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                SyncState.is_online,
                rx.el.div(
                    rx.el.div(class_name="w-2 h-2 rounded-full bg-green-500 mr-2"),
                    rx.el.span(
                        "Online", class_name="text-xs font-medium text-green-700"
                    ),
                    class_name="flex items-center bg-green-100 px-2 py-1 rounded-lg",
                ),
                rx.el.div(
                    rx.el.div(class_name="w-2 h-2 rounded-full bg-red-500 mr-2"),
                    rx.el.span(
                        "Offline", class_name="text-xs font-medium text-red-700"
                    ),
                    class_name="flex items-center bg-red-100 px-2 py-1 rounded-lg",
                ),
            ),
            class_name="mr-2",
        ),
        rx.el.button(
            rx.cond(
                SyncState.is_syncing,
                rx.icon("loader", class_name="w-5 h-5 text-[#0EA5E9] animate-spin"),
                rx.el.div(
                    rx.icon("refresh-cw", class_name="w-5 h-5 text-gray-600"),
                    rx.cond(
                        SyncState.pending_count > 0,
                        rx.el.span(
                            SyncState.pending_count,
                            class_name="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center",
                        ),
                    ),
                    class_name="relative",
                ),
            ),
            on_click=SyncState.sync_data,
            disabled=~SyncState.is_online | SyncState.is_syncing,
            class_name="p-2 hover:bg-gray-100 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
            title="Sync Now",
        ),
        class_name="flex items-center",
    )