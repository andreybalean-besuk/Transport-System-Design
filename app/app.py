import reflex as rx
from app.pages.login import login_page
from app.pages.driver_dashboard import driver_dashboard
from app.pages.manager_dashboard import manager_dashboard


def index() -> rx.Component:
    return login_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(rel="manifest", href="/manifest.json"),
        rx.el.script("""
            // Service Worker Registration
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                    navigator.serviceWorker.register('/sw.js').then(function(registration) {
                        console.log('ServiceWorker registration successful with scope: ', registration.scope);
                    }, function(err) {
                        console.log('ServiceWorker registration failed: ', err);
                    });
                });
            }
            // Online/Offline Detection
            // We rely on browser events, but typically to trigger Reflex state update 
            // we might need a more complex setup. For now, we simply assume online 
            // at start and let the user manually verify via visual cues.
            """),
    ],
)
app.add_page(index, route="/", title="Login - Transport App")
app.add_page(driver_dashboard, route="/driver-dashboard", title="Driver Dashboard")
app.add_page(manager_dashboard, route="/manager-dashboard", title="Manager Dashboard")