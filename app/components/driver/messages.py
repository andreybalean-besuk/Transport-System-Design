import reflex as rx
from app.states.driver_state import DriverState


def message_item(msg: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(msg["folder"] == "inbox", "mail", "send"),
                    class_name="w-5 h-5 text-gray-400 mr-3",
                ),
                rx.el.div(
                    rx.el.h4(
                        msg["subject"], class_name="font-bold text-gray-800 text-sm"
                    ),
                    rx.el.p(
                        rx.cond(
                            msg["folder"] == "outbox",
                            f"To: {msg['recipient']}",
                            f"From: {msg['sender']}",
                        ),
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-start",
            ),
            rx.el.span(
                msg["timestamp"].split("T")[0],
                class_name="text-xs text-gray-400 whitespace-nowrap ml-2",
            ),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.p(msg["body"], class_name="text-sm text-gray-600 pl-8 line-clamp-2"),
        class_name="p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer last:border-0",
    )


def messages_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Messages", class_name="text-xl font-bold text-gray-900"),
            rx.el.p("Communication center", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Compose Message", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            rx.el.input(
                placeholder="Subject",
                on_change=DriverState.set_msg_subject,
                class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none mb-3",
                default_value=DriverState.msg_subject,
            ),
            rx.el.textarea(
                placeholder="Type your message to manager...",
                on_change=DriverState.set_msg_body,
                class_name="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 focus:ring-2 focus:ring-[#0EA5E9] focus:border-transparent outline-none min-h-[100px] mb-3",
                default_value=DriverState.msg_body,
            ),
            rx.el.button(
                rx.icon("send", class_name="w-4 h-4 mr-2"),
                "Send Message",
                on_click=DriverState.send_message,
                class_name="w-full py-3 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md flex items-center justify-center transition-all",
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 mb-6",
        ),
        rx.el.div(
            rx.el.h3(
                "Recent Messages",
                class_name="text-lg font-semibold text-gray-800 mb-4 px-6 pt-6",
            ),
            rx.el.div(
                rx.cond(
                    DriverState.messages.length() > 0,
                    rx.foreach(DriverState.messages, message_item),
                    rx.el.div(
                        "No messages found.",
                        class_name="p-6 text-center text-gray-500 italic",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden",
        ),
        class_name="flex flex-col",
    )