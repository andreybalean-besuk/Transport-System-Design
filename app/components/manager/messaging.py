import reflex as rx
from app.states.manager_state import ManagerState


def message_row(msg) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.cond(msg.folder == "inbox", "mail", "send"),
                class_name="w-5 h-5 text-gray-400 mr-3",
            ),
            rx.el.div(
                rx.el.span(
                    rx.cond(msg.folder == "inbox", msg.sender, msg.recipient),
                    class_name="font-bold text-gray-800 text-sm",
                ),
                rx.el.p(msg.subject, class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(msg.timestamp.split("T")[0], class_name="text-xs text-gray-400"),
        class_name="flex justify-between items-center p-3 border-b border-gray-50 hover:bg-gray-50 transition-colors",
    )


def messaging() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Messaging Center", class_name="text-xl font-bold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.el.h3(
                    "Compose Message",
                    class_name="text-sm font-bold text-gray-700 mb-3 uppercase",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("All Drivers (Broadcast)", value="All"),
                        rx.foreach(
                            ManagerState.drivers,
                            lambda d: rx.el.option(d.name, value=d.id),
                        ),
                        on_change=ManagerState.set_msg_recipient,
                        class_name="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none bg-white mb-3",
                    ),
                    rx.el.input(
                        placeholder="Subject",
                        on_change=ManagerState.set_msg_subject,
                        class_name="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none mb-3",
                        default_value=ManagerState.msg_subject,
                    ),
                    rx.el.textarea(
                        placeholder="Message body...",
                        on_change=ManagerState.set_msg_body,
                        class_name="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0EA5E9] outline-none min-h-[100px] mb-3",
                        default_value=ManagerState.msg_body,
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="w-4 h-4 mr-2"),
                        "Send Message",
                        on_click=ManagerState.send_message,
                        class_name="w-full py-3 bg-[#0EA5E9] hover:bg-[#0284C7] text-white font-bold rounded-xl shadow-md transition-all flex items-center justify-center",
                    ),
                    class_name="bg-gray-50 p-4 rounded-xl mb-6",
                ),
            ),
            rx.el.div(
                rx.el.h3(
                    "Message History",
                    class_name="text-sm font-bold text-gray-700 mb-3 uppercase",
                ),
                rx.el.div(
                    rx.cond(
                        ManagerState.messages.length() > 0,
                        rx.foreach(ManagerState.messages, message_row),
                        rx.el.p(
                            "No messages found.",
                            class_name="text-gray-500 italic text-center py-8",
                        ),
                    ),
                    class_name="border border-gray-100 rounded-xl overflow-hidden",
                ),
            ),
            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-200",
        ),
        class_name="w-full animate-fadeIn",
    )