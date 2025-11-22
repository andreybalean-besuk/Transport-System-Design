import reflex as rx
import asyncio
from datetime import datetime
import json


class SyncState(rx.State):
    is_online: bool = True
    is_syncing: bool = False
    last_sync_time: str = "Never"
    pending_count: int = 0
    show_install_banner: bool = True

    @rx.event
    def set_online_status(self, status: bool):
        self.is_online = status
        if status and self.pending_count > 0:
            return SyncState.sync_data

    @rx.event
    def close_install_banner(self):
        self.show_install_banner = False

    @rx.event
    async def check_pending_count(self):
        from app.states.driver_state import DriverState

        driver_state = await self.get_state(DriverState)
        count = 0
        for check in driver_state.checks:
            if not getattr(check, "synced", True):
                count += 1
        for ts in driver_state.timesheets:
            if not getattr(ts, "synced", True):
                count += 1
        self.pending_count = count

    @rx.event(background=True)
    async def sync_data(self):
        async with self:
            if not self.is_online:
                yield rx.toast.error("Cannot sync while offline.")
                return
            self.is_syncing = True
            yield
        await asyncio.sleep(1.5)
        async with self:
            from app.states.driver_state import DriverState

            driver_state = await self.get_state(DriverState)
            updated_checks = []
            synced_count = 0
            for check in driver_state.checks:
                if not getattr(check, "synced", True):
                    check.synced = True
                    synced_count += 1
                updated_checks.append(check)
            driver_state.checks = updated_checks
            updated_timesheets = []
            for ts in driver_state.timesheets:
                if not getattr(ts, "synced", True):
                    ts.synced = True
                    synced_count += 1
                updated_timesheets.append(ts)
            driver_state.timesheets = updated_timesheets
            driver_state.checks_json = json.dumps(
                [c.dict() for c in driver_state.checks]
            )
            driver_state.timesheets_json = json.dumps(
                [t.dict() for t in driver_state.timesheets]
            )
            self.last_sync_time = datetime.now().strftime("%H:%M")
            self.is_syncing = False
            self.pending_count = 0
            if synced_count > 0:
                yield rx.toast.success(f"Successfully synced {synced_count} items.")
            else:
                yield rx.toast.info("All data is already up to date.")