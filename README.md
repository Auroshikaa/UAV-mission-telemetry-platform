# UAV Mission Telemetry Platform

Built a simulated UAV fleet monitoring system that tracks real-time flight telemetry, stores mission data, and visualizes fleet health through a live ground control dashboard.

I built this because I wanted a project that felt closer to aerospace/defense systems than typical software projects. After building my industrial monitoring project, I realized the same architecture could be applied to mission systems — but with more interesting problems like fleet coordination, mission phases, GPS failures, communication loss, and battery constraints.

This project simulates multiple UAVs completing different mission types while sending telemetry back to a ground control system.

---

## What the system does

Each UAV continuously sends:

- altitude
- speed
- battery percentage
- motor temperature
- GPS coordinates
- signal strength
- mission phase
- fault status
- health status

Example mission phases:

- Pre-flight  
- Takeoff  
- Climb  
- Cruise  
- Surveillance  
- Return Home  
- Landing  
- Mission Complete  

---

## Fleet simulation

The platform currently simulates multiple UAVs:

- UAV_MAVERICK_01 → reconnaissance  
- UAV_ICEMAN_02 → high altitude surveillance  
- UAV_ROOSTER_03 → rapid response  
- UAV_PHOENIX_04 → communications relay  

Each UAV has:

- different fault probabilities  
- separate battery levels  
- separate telemetry streams  
- different mission profiles  

---

## Fault simulation

I added failure scenarios to make the simulation more realistic:

- GPS signal loss  
- low battery warnings  
- weak communication signal  
- motor overheating  

These faults automatically trigger warning/critical health states.

One small detail I liked adding:
when GPS fails, the simulator stops sending valid coordinates.

---

## Architecture

```text
UAV Fleet Simulator
        ↓
Flask Ground Control API
        ↓
SQLite Mission Database
        ↓
Streamlit Ground Control Dashboard
```

---

## Why I used this architecture

I didn’t want UAVs writing directly into a database.

Using an API layer makes the system more modular and closer to how real telemetry systems work.

It also made it easier to scale from one UAV to multiple UAVs later.

---

## Dashboard features

The dashboard allows you to:

- filter by UAV  
- monitor current mission phase  
- track battery levels  
- monitor altitude trends  
- monitor signal strength  
- view active faults  
- review historical mission logs  

---

## Tech stack

- Python  
- Flask  
- SQLite  
- Streamlit  
- Pandas  
- Requests  

---

## Biggest things I learned

- designing systems with multiple moving parts  
- thinking through failure scenarios  
- building reusable architecture patterns  
- scaling from single-device systems to fleet systems  
- how telemetry systems can apply across completely different industries  

---

## Running the project

```bash
python ground_control_backend.py
python uav_telemetry_simulator.py
streamlit run ground_control_dashboard.py
```

---

## Future improvements

If I keep building this further, I’d probably add:

- mission replay  
- live map tracking  
- real hardware integration  
- swarm coordination logic  
- cloud deployment  

---

## Why this project was fun

This started as:

"what if I built something more defense-oriented?"

And somehow turned into a UAV fleet simulator named after Top Gun characters.

No regrets.
