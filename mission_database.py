import sqlite3

DATABASE_NAME = "uav_mission.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uav_id TEXT NOT NULL,
        mission_type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        mission_phase TEXT NOT NULL,
        altitude_m REAL NOT NULL,
        speed_kmh REAL NOT NULL,
        battery_percent REAL NOT NULL,
        motor_temp_c REAL NOT NULL,
        gps_latitude REAL,
        gps_longitude REAL,
        signal_strength REAL NOT NULL,
        fault TEXT NOT NULL,
        health_status TEXT NOT NULL
    )
""")

    connection.commit()
    connection.close()


def insert_telemetry(data):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO telemetry (
        uav_id,
        mission_type,
        timestamp,
        mission_phase,
        altitude_m,
        speed_kmh,
        battery_percent,
        motor_temp_c,
        gps_latitude,
        gps_longitude,
        signal_strength,
        fault,
        health_status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    data["uav_id"],
    data["mission_type"],
    data["timestamp"],
    data["mission_phase"],
    data["altitude_m"],
    data["speed_kmh"],
    data["battery_percent"],
    data["motor_temp_c"],
    data["gps_latitude"],
    data["gps_longitude"],
    data["signal_strength"],
    data["fault"],
    data["health_status"]
))

    connection.commit()
    connection.close()