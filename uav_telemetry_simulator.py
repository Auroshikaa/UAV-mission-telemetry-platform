import random
import time
import json
import requests
from datetime import datetime


API_URL = "http://127.0.0.1:5000/telemetry"

MISSION_PHASES = [
    "PRE_FLIGHT",
    "TAKEOFF",
    "CLIMB",
    "CRUISE",
    "SURVEILLANCE",
    "RETURN_HOME",
    "LANDING",
    "MISSION_COMPLETE"
]

UAV_FLEET = [
    {
        "uav_id": "UAV_MAVERICK_01",
        "mission_type": "reconnaissance",
        "base_latitude": 43.70,
        "base_longitude": -79.35,
        "fault_chance": 0.10,
    },
    {
        "uav_id": "UAV_ICEMAN_02",
        "mission_type": "high_altitude_surveillance",
        "base_latitude": 43.72,
        "base_longitude": -79.38,
        "fault_chance": 0.07,
    },
    {
        "uav_id": "UAV_ROOSTER_03",
        "mission_type": "rapid_response",
        "base_latitude": 43.68,
        "base_longitude": -79.32,
        "fault_chance": 0.14,
    },
    {
        "uav_id": "UAV_PHOENIX_04",
        "mission_type": "communications_relay",
        "base_latitude": 43.75,
        "base_longitude": -79.41,
        "fault_chance": 0.12,
    },
]


def generate_fault(uav: dict) -> str:
    roll = random.random()

    if roll < uav["fault_chance"] * 0.25:
        return "GPS_SIGNAL_LOSS"
    elif roll < uav["fault_chance"] * 0.50:
        return "LOW_BATTERY_WARNING"
    elif roll < uav["fault_chance"] * 0.75:
        return "MOTOR_OVERHEAT"
    elif roll < uav["fault_chance"]:
        return "COMMUNICATION_WEAK_SIGNAL"
    else:
        return "NONE"


def get_battery_drain(phase: str) -> float:
    if phase == "PRE_FLIGHT":
        return random.uniform(0.5, 1.0)
    elif phase == "TAKEOFF":
        return random.uniform(4.0, 8.0)
    elif phase == "CLIMB":
        return random.uniform(5.0, 9.0)
    elif phase == "CRUISE":
        return random.uniform(2.0, 4.0)
    elif phase == "SURVEILLANCE":
        return random.uniform(3.0, 5.0)
    elif phase == "RETURN_HOME":
        return random.uniform(2.0, 4.0)
    elif phase == "LANDING":
        return random.uniform(1.0, 3.0)
    else:
        return 0.0


def classify_health(battery: float, motor_temp: float, signal_strength: float, fault: str) -> str:
    if fault in ["GPS_SIGNAL_LOSS", "MOTOR_OVERHEAT"]:
        return "CRITICAL"
    elif battery < 25 or motor_temp > 85 or signal_strength < 40:
        return "WARNING"
    elif fault != "NONE":
        return "WARNING"
    else:
        return "NORMAL"


def generate_phase_telemetry(uav: dict, phase: str, battery: float) -> dict:
    if phase == "PRE_FLIGHT":
        altitude = 0
        speed = 0
        motor_temp = random.uniform(25, 35)

    elif phase == "TAKEOFF":
        altitude = random.uniform(50, 300)
        speed = random.uniform(40, 90)
        motor_temp = random.uniform(45, 65)

    elif phase == "CLIMB":
        altitude = random.uniform(300, 1200)
        speed = random.uniform(90, 160)
        motor_temp = random.uniform(55, 75)

    elif phase == "CRUISE":
        altitude = random.uniform(1200, 1600)
        speed = random.uniform(150, 220)
        motor_temp = random.uniform(60, 78)

    elif phase == "SURVEILLANCE":
        altitude = random.uniform(1000, 1400)
        speed = random.uniform(60, 110)
        motor_temp = random.uniform(58, 80)

    elif phase == "RETURN_HOME":
        altitude = random.uniform(700, 1200)
        speed = random.uniform(130, 190)
        motor_temp = random.uniform(60, 82)

    elif phase == "LANDING":
        altitude = random.uniform(0, 300)
        speed = random.uniform(20, 70)
        motor_temp = random.uniform(45, 65)

    else:
        altitude = 0
        speed = 0
        motor_temp = random.uniform(30, 45)

    gps_latitude = round(uav["base_latitude"] + random.uniform(-0.05, 0.05), 6)
    gps_longitude = round(uav["base_longitude"] + random.uniform(-0.05, 0.05), 6)
    signal_strength = round(random.uniform(30, 100), 2)

    fault = generate_fault(uav)
    health_status = classify_health(
        battery=battery,
        motor_temp=motor_temp,
        signal_strength=signal_strength,
        fault=fault
    )

    if fault == "GPS_SIGNAL_LOSS":
        gps_latitude = None
        gps_longitude = None

    return {
        "uav_id": uav["uav_id"],
        "mission_type": uav["mission_type"],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mission_phase": phase,
        "altitude_m": round(altitude, 2),
        "speed_kmh": round(speed, 2),
        "battery_percent": round(battery, 2),
        "motor_temp_c": round(motor_temp, 2),
        "gps_latitude": gps_latitude,
        "gps_longitude": gps_longitude,
        "signal_strength": signal_strength,
        "fault": fault,
        "health_status": health_status
    }


def send_telemetry(telemetry: dict) -> None:
    try:
        response = requests.post(
            API_URL,
            json=telemetry
        )

        print("Sent telemetry:")
        print(json.dumps(telemetry, indent=2))
        print("Ground control response:")
        print(response.json())
        print("-" * 50)

    except requests.exceptions.RequestException as error:
        print("Failed to send telemetry:", error)


def main() -> None:
    print("Starting UAV Fleet Telemetry Simulator...\n")

    fleet_battery = {
        uav["uav_id"]: 100.0
        for uav in UAV_FLEET
    }

    while True:
        for phase in MISSION_PHASES:
            for uav in UAV_FLEET:
                uav_id = uav["uav_id"]

                battery_drain = get_battery_drain(phase)
                fleet_battery[uav_id] = max(0, fleet_battery[uav_id] - battery_drain)

                telemetry = generate_phase_telemetry(
                    uav=uav,
                    phase=phase,
                    battery=fleet_battery[uav_id]
                )

                send_telemetry(telemetry)

            time.sleep(3)

        print("Fleet mission cycle complete. Restarting simulation...\n")

        fleet_battery = {
            uav["uav_id"]: 100.0
            for uav in UAV_FLEET
        }


if __name__ == "__main__":
    main()