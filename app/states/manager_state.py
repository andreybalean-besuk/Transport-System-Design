import reflex as rx
import json
import uuid
import logging
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.states.driver_state import DailyCheck, TimesheetEntry, Message


class Driver(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    license_number: str
    status: str = "Active"
    joined_date: str


class Vehicle(BaseModel):
    id: str
    make: str
    model: str
    year: str
    plate: str
    status: str = "Active"
    assigned_driver_id: Optional[str] = None


class MaintenanceRecord(BaseModel):
    id: str
    vehicle_id: str
    type: str
    scheduled_date: str
    status: str = "Scheduled"
    description: str


class ManagerState(rx.State):
    checks_json: str = rx.LocalStorage("[]", name="driver_checks")
    timesheets_json: str = rx.LocalStorage("[]", name="driver_timesheets")
    messages_json: str = rx.LocalStorage("[]", name="driver_messages")
    drivers_json: str = rx.LocalStorage("[]", name="manager_drivers")
    vehicles_json: str = rx.LocalStorage("[]", name="manager_vehicles")
    maintenance_json: str = rx.LocalStorage("[]", name="manager_maintenance")
    current_tab: str = "overview"
    checks: list[DailyCheck] = []
    timesheets: list[TimesheetEntry] = []
    messages: list[Message] = []
    drivers: list[Driver] = []
    vehicles: list[Vehicle] = []
    maintenance: list[MaintenanceRecord] = []
    overview_search: str = ""
    timesheet_filter: str = "All"
    new_driver_name: str = ""
    new_driver_email: str = ""
    new_driver_phone: str = ""
    new_driver_license: str = ""
    new_vehicle_make: str = ""
    new_vehicle_model: str = ""
    new_vehicle_year: str = ""
    new_vehicle_plate: str = ""
    new_maint_vehicle_id: str = ""
    new_maint_type: str = ""
    new_maint_date: str = ""
    new_maint_desc: str = ""
    msg_subject: str = ""
    msg_body: str = ""
    msg_recipient_id: str = "All"

    def _load_data(self):
        try:
            self.checks = [DailyCheck(**item) for item in json.loads(self.checks_json)]
            self.timesheets = [
                TimesheetEntry(**item) for item in json.loads(self.timesheets_json)
            ]
            self.messages = [Message(**item) for item in json.loads(self.messages_json)]
            drivers_data = json.loads(self.drivers_json)
            if not drivers_data:
                self.drivers = []
            else:
                self.drivers = [Driver(**item) for item in drivers_data]
            vehicles_data = json.loads(self.vehicles_json)
            if not vehicles_data:
                self.vehicles = []
            else:
                self.vehicles = [Vehicle(**item) for item in vehicles_data]
            maint_data = json.loads(self.maintenance_json)
            if not maint_data:
                self.maintenance = []
            else:
                self.maintenance = [MaintenanceRecord(**item) for item in maint_data]
        except Exception as e:
            logging.exception(f"Error loading manager data: {e}")

    @rx.event
    def on_load(self):
        self._load_data()

    @rx.event
    def set_current_tab(self, tab: str):
        self.current_tab = tab

    @rx.event
    def set_overview_search(self, val: str):
        self.overview_search = val

    @rx.event
    def approve_timesheet(self, ts_id: str):
        self._load_data()
        for ts in self.timesheets:
            if ts.id == ts_id:
                ts.status = "Approved"
        self.timesheets_json = json.dumps([t.dict() for t in self.timesheets])
        return rx.toast.success("Timesheet approved")

    @rx.event
    def reject_timesheet(self, ts_id: str):
        self._load_data()
        for ts in self.timesheets:
            if ts.id == ts_id:
                ts.status = "Rejected"
        self.timesheets_json = json.dumps([t.dict() for t in self.timesheets])
        return rx.toast.error("Timesheet rejected")

    @rx.event
    def set_new_driver_name(self, val: str):
        self.new_driver_name = val

    @rx.event
    def set_new_driver_email(self, val: str):
        self.new_driver_email = val

    @rx.event
    def set_new_driver_phone(self, val: str):
        self.new_driver_phone = val

    @rx.event
    def set_new_driver_license(self, val: str):
        self.new_driver_license = val

    @rx.event
    def add_driver(self):
        if not all(
            [self.new_driver_name, self.new_driver_email, self.new_driver_license]
        ):
            return rx.toast.error("Name, Email and License are required")
        new_driver = Driver(
            id=str(uuid.uuid4()),
            name=self.new_driver_name,
            email=self.new_driver_email,
            phone=self.new_driver_phone,
            license_number=self.new_driver_license,
            joined_date=datetime.now().strftime("%Y-%m-%d"),
        )
        self.drivers.append(new_driver)
        self.drivers_json = json.dumps([d.dict() for d in self.drivers])
        self.new_driver_name = ""
        self.new_driver_email = ""
        self.new_driver_phone = ""
        self.new_driver_license = ""
        return rx.toast.success("Driver added successfully")

    @rx.event
    def set_new_vehicle_make(self, val: str):
        self.new_vehicle_make = val

    @rx.event
    def set_new_vehicle_model(self, val: str):
        self.new_vehicle_model = val

    @rx.event
    def set_new_vehicle_year(self, val: str):
        self.new_vehicle_year = val

    @rx.event
    def set_new_vehicle_plate(self, val: str):
        self.new_vehicle_plate = val

    @rx.event
    def add_vehicle(self):
        if not all(
            [self.new_vehicle_make, self.new_vehicle_model, self.new_vehicle_plate]
        ):
            return rx.toast.error("Make, Model and Plate are required")
        new_vehicle = Vehicle(
            id=str(uuid.uuid4()),
            make=self.new_vehicle_make,
            model=self.new_vehicle_model,
            year=self.new_vehicle_year,
            plate=self.new_vehicle_plate,
        )
        self.vehicles.append(new_vehicle)
        self.vehicles_json = json.dumps([v.dict() for v in self.vehicles])
        self.new_vehicle_make = ""
        self.new_vehicle_model = ""
        self.new_vehicle_year = ""
        self.new_vehicle_plate = ""
        return rx.toast.success("Vehicle added successfully")

    @rx.event
    def set_new_maint_vehicle_id(self, val: str):
        self.new_maint_vehicle_id = val

    @rx.event
    def set_new_maint_type(self, val: str):
        self.new_maint_type = val

    @rx.event
    def set_new_maint_date(self, val: str):
        self.new_maint_date = val

    @rx.event
    def set_new_maint_desc(self, val: str):
        self.new_maint_desc = val

    @rx.event
    def schedule_maintenance(self):
        if not all(
            [self.new_maint_vehicle_id, self.new_maint_type, self.new_maint_date]
        ):
            return rx.toast.error("Vehicle, Type and Date are required")
        new_maint = MaintenanceRecord(
            id=str(uuid.uuid4()),
            vehicle_id=self.new_maint_vehicle_id,
            type=self.new_maint_type,
            scheduled_date=self.new_maint_date,
            description=self.new_maint_desc,
        )
        self.maintenance.append(new_maint)
        self.maintenance_json = json.dumps([m.dict() for m in self.maintenance])
        self.new_maint_desc = ""
        self.new_maint_type = ""
        return rx.toast.success("Maintenance scheduled")

    @rx.event
    def set_msg_subject(self, val: str):
        self.msg_subject = val

    @rx.event
    def set_msg_body(self, val: str):
        self.msg_body = val

    @rx.event
    def set_msg_recipient(self, val: str):
        self.msg_recipient_id = val

    @rx.event
    def send_message(self):
        if not self.msg_subject or not self.msg_body:
            return rx.toast.error("Subject and body are required")
        self._load_data()
        recipient_name = "All Drivers"
        if self.msg_recipient_id != "All":
            for d in self.drivers:
                if d.id == self.msg_recipient_id:
                    recipient_name = d.name
                    break
        new_msg = Message(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender="Manager",
            recipient=recipient_name,
            subject=self.msg_subject,
            body=self.msg_body,
            is_read=False,
            folder="inbox",
        )
        self.messages.insert(0, new_msg)
        self.messages_json = json.dumps([m.dict() for m in self.messages])
        self.msg_subject = ""
        self.msg_body = ""
        return rx.toast.success("Message sent successfully")