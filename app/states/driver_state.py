import reflex as rx
from datetime import datetime
import json
import uuid
import logging
from typing import Optional
from pydantic import BaseModel
from app.states.sync_state import SyncState


class DailyCheck(BaseModel):
    id: str
    timestamp: str
    vehicle_id: str
    odometer: str
    fuel_level: int
    checklist: dict[str, bool]
    fluids: dict[str, str]
    defects: str
    driver_signature: str
    synced: bool = True


class TimesheetEntry(BaseModel):
    id: str
    date: str
    clock_in: Optional[str] = None
    clock_out: Optional[str] = None
    breaks: list[dict[str, str]] = []
    total_hours: float = 0.0
    status: str = "Pending"
    synced: bool = True


class Message(BaseModel):
    id: str
    timestamp: str
    sender: str
    recipient: str
    subject: str
    body: str
    is_read: bool = False
    folder: str = "inbox"


class DriverState(rx.State):
    checks_json: str = rx.LocalStorage("[]", name="driver_checks")
    timesheets_json: str = rx.LocalStorage("[]", name="driver_timesheets")
    messages_json: str = rx.LocalStorage("[]", name="driver_messages")
    current_tab: str = "checks"
    vehicle_id: str = ""
    odometer: str = ""
    fuel_level: int = 50
    defects: str = ""
    driver_signature: str = ""
    check_lights: bool = False
    check_tires: bool = False
    check_brakes: bool = False
    check_mirrors: bool = False
    check_windshield: bool = False
    check_wipers: bool = False
    check_horn: bool = False
    check_seatbelts: bool = False
    fluid_oil: str = "OK"
    fluid_coolant: str = "OK"
    fluid_brake: str = "OK"
    fluid_washer: str = "OK"
    msg_recipient: str = "Manager"
    msg_subject: str = ""
    msg_body: str = ""
    checks: list[DailyCheck] = []
    timesheets: list[TimesheetEntry] = []
    messages: list[Message] = []

    def _load_data(self):
        """Helper to load data from JSON strings"""
        try:
            self.checks = [DailyCheck(**item) for item in json.loads(self.checks_json)]
        except Exception as e:
            logging.exception(f"Error loading checks: {e}")
            self.checks = []
        try:
            self.timesheets = [
                TimesheetEntry(**item) for item in json.loads(self.timesheets_json)
            ]
        except Exception as e:
            logging.exception(f"Error loading timesheets: {e}")
            self.timesheets = []
        try:
            self.messages = [Message(**item) for item in json.loads(self.messages_json)]
        except Exception as e:
            logging.exception(f"Error loading messages: {e}")
            self.messages = []

    @rx.event
    def on_load(self):
        self._load_data()

    @rx.event
    def set_vehicle_id(self, val: str):
        self.vehicle_id = val

    @rx.event
    def set_odometer(self, val: str):
        self.odometer = val

    @rx.event
    def set_fuel_level(self, val: int):
        self.fuel_level = val

    @rx.event
    def set_defects(self, val: str):
        self.defects = val

    @rx.event
    def set_driver_signature(self, val: str):
        self.driver_signature = val

    @rx.event
    def toggle_check(self, item: str):
        if item == "lights":
            self.check_lights = not self.check_lights
        elif item == "tires":
            self.check_tires = not self.check_tires
        elif item == "brakes":
            self.check_brakes = not self.check_brakes
        elif item == "mirrors":
            self.check_mirrors = not self.check_mirrors
        elif item == "windshield":
            self.check_windshield = not self.check_windshield
        elif item == "wipers":
            self.check_wipers = not self.check_wipers
        elif item == "horn":
            self.check_horn = not self.check_horn
        elif item == "seatbelts":
            self.check_seatbelts = not self.check_seatbelts

    @rx.event
    def set_fluid(self, fluid: str, val: str):
        if fluid == "oil":
            self.fluid_oil = val
        elif fluid == "coolant":
            self.fluid_coolant = val
        elif fluid == "brake":
            self.fluid_brake = val
        elif fluid == "washer":
            self.fluid_washer = val

    @rx.event
    def submit_check(self):
        if not self.vehicle_id or not self.odometer or (not self.driver_signature):
            return rx.toast.error(
                "Please fill in all required fields (Vehicle ID, Odometer, Signature)"
            )
        self._load_data()
        new_check = DailyCheck(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            vehicle_id=self.vehicle_id,
            odometer=self.odometer,
            fuel_level=self.fuel_level,
            checklist={
                "lights": self.check_lights,
                "tires": self.check_tires,
                "brakes": self.check_brakes,
                "mirrors": self.check_mirrors,
                "windshield": self.check_windshield,
                "wipers": self.check_wipers,
                "horn": self.check_horn,
                "seatbelts": self.check_seatbelts,
            },
            fluids={
                "oil": self.fluid_oil,
                "coolant": self.fluid_coolant,
                "brake": self.fluid_brake,
                "washer": self.fluid_washer,
            },
            defects=self.defects,
            driver_signature=self.driver_signature,
            synced=False,
        )
        self.checks.insert(0, new_check)
        self.checks_json = json.dumps([c.dict() for c in self.checks])
        self.vehicle_id = ""
        self.odometer = ""
        self.defects = ""
        self.driver_signature = ""
        self.check_lights = False
        yield SyncState.check_pending_count
        self.check_tires = False
        self.check_brakes = False
        self.check_mirrors = False
        self.check_windshield = False
        self.check_wipers = False
        self.check_horn = False
        self.check_seatbelts = False
        return rx.toast.success("Daily check submitted successfully")

    @rx.event
    def clock_in(self):
        self._load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        for ts in self.timesheets:
            if ts.date == today and ts.status == "Active":
                return rx.toast.error("You are already clocked in for today.")
        new_entry = TimesheetEntry(
            id=str(uuid.uuid4()),
            date=today,
            clock_in=datetime.now().isoformat(),
            status="Active",
        )
        self.timesheets.insert(0, new_entry)
        self.timesheets_json = json.dumps([t.dict() for t in self.timesheets])
        yield SyncState.check_pending_count
        return rx.toast.success("Clocked in successfully")

    @rx.event
    def clock_out(self):
        self._load_data()
        for ts in self.timesheets:
            if ts.status == "Active":
                ts.clock_out = datetime.now().isoformat()
                ts.status = "Completed"
                start = datetime.fromisoformat(ts.clock_in)
                end = datetime.fromisoformat(ts.clock_out)
                duration = (end - start).total_seconds() / 3600
                break_duration = 0
                for b in ts.breaks:
                    if "end" in b:
                        b_start = datetime.fromisoformat(b["start"])
                        b_end = datetime.fromisoformat(b["end"])
                        break_duration += (b_end - b_start).total_seconds() / 3600
                net_hours = max(0.0, duration - break_duration)
                if net_hours > 0:
                    ts.total_hours = max(0.01, round(net_hours, 2))
                else:
                    ts.total_hours = 0.0
                ts.synced = False
                self.timesheets_json = json.dumps([t.dict() for t in self.timesheets])
                yield SyncState.check_pending_count
                return rx.toast.success(f"Clocked out. Total hours: {ts.total_hours}")
        return rx.toast.error("No active shift found")

    @rx.event
    def start_break(self):
        self._load_data()
        for ts in self.timesheets:
            if ts.status == "Active":
                if ts.breaks and "end" not in ts.breaks[-1]:
                    return rx.toast.error("You are already on a break")
                ts.breaks.append({"start": datetime.now().isoformat()})
                self.timesheets_json = json.dumps([t.dict() for t in self.timesheets])
                return rx.toast.info("Break started")
        return rx.toast.error("No active shift found")

    @rx.event
    def end_break(self):
        self._load_data()
        for ts in self.timesheets:
            if ts.status == "Active":
                if ts.breaks and "end" not in ts.breaks[-1]:
                    ts.breaks[-1]["end"] = datetime.now().isoformat()
                    self.timesheets_json = json.dumps(
                        [t.dict() for t in self.timesheets]
                    )
                    return rx.toast.info("Break ended")
                return rx.toast.error("You are not currently on a break")
        return rx.toast.error("No active shift found")

    @rx.event
    def set_msg_subject(self, val: str):
        self.msg_subject = val

    @rx.event
    def set_msg_body(self, val: str):
        self.msg_body = val

    @rx.event
    def send_message(self):
        if not self.msg_subject or not self.msg_body:
            return rx.toast.error("Subject and body are required")
        self._load_data()
        new_msg = Message(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender="Driver",
            recipient="Manager",
            subject=self.msg_subject,
            body=self.msg_body,
            is_read=True,
            folder="outbox",
        )
        self.messages.insert(0, new_msg)
        self.messages_json = json.dumps([m.dict() for m in self.messages])
        self.msg_subject = ""
        self.msg_body = ""
        return rx.toast.success("Message sent")