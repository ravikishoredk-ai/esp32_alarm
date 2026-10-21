from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid

app = FastAPI()

class AlarmInput(BaseModel):
    time: str

# In-memory database to store multiple alarms
alarms_db = []

# Serve the HTML Dashboard
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("index.html", "r") as file:
        return file.read()

# API to get all alarms
@app.get("/api/alarms")
async def get_alarms():
    return alarms_db

# API to add a new alarm
@app.post("/api/alarms")
async def add_alarm(alarm: AlarmInput):
    new_alarm = {"id": str(uuid.uuid4()), "time": alarm.time, "active": True}
    alarms_db.append(new_alarm)
    return new_alarm

# API to delete an alarm
@app.delete("/api/alarms/{alarm_id}")
async def delete_alarm(alarm_id: str):
    global alarms_db
    alarms_db = [a for a in alarms_db if a["id"] != alarm_id]
    return {"status": "success"}

# API for the ESP32 to check active alarms
@app.get("/api/esp-alarms")
async def esp_check_alarms():
    active_times = [a["time"] for a in alarms_db if a["active"]]
    return {"alarms": active_times}
