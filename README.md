
# 🍺 **Fermentation Controller**  

A modern, scalable, and automated fermentation process control system built to monitor and regulate fermentation tanks, providing brewers with precision and control over their brewing process. Designed for breweries, home brewers, and fermentation enthusiasts, this system leverages **Raspberry Pi**, **UniPi 1.1**, and **Django** to deliver seamless automation, advanced monitoring, and a user-friendly dashboard.

---

## 📋 **Project Overview**

The **Fermentation Controller** is an advanced software-hardware solution that regulates temperatures and manages the operation of fermentation tanks during brewing. It integrates temperature sensors, relays, and valves to automate critical processes like cooling, pumping, and safety measures. The project emphasizes **scalability**, **modularity**, and an attractive graphical interface for real-time control.

---

## ⚙️ **Features**

1. **Temperature Monitoring and Control**
   - Integration with DS18B20 temperature sensors for precise temperature monitoring.
   - Automatic regulation of cooling systems (chiller activation).
   - Real-time display and logging of tank temperatures.

2. **Valve and Pump Control**
   - Manage up to 8 individual valves for each tank.
   - Digital input for physical control of pumps.
   - Relay-controlled operation of chillers and pumps.

3. **Safety Mechanisms**
   - Digital input with a dedicated **"total stop"** button for emergency shutdown.
   - Real-time monitoring and feedback to prevent process errors.

4. **User-Friendly Dashboard**
   - Built using **Django** to provide a clean, responsive web interface.
   - Display live status of tanks, valves, chillers, and pumps.
   - Monitor historical data and logs for analysis.

5. **Data Logging and Management**
   - Data persistence using **SQLite**.
   - Log temperature trends, valve activity, and pump status.
   - Export historical data for analysis.

6. **Modular Architecture**
   - Scalable design to manage additional tanks and equipment.
   - Easy integration of **Modbus RTU** modules (e.g., xG18 for temperature sensors).

7. **Future-Ready**
   - Prepared for dynamic UI scaling.
   - Modular setup allows easy expansion to new fermentation tanks and equipment.
   - Fault simulation and notification systems (coming soon).

---

## 🖥️ **Technologies Used**

- **Hardware**
  - Raspberry Pi with UniPi 1.1 hardware.
  - EMO-R8 module for relays.
  - DS18B20 sensors for temperature monitoring.
  - xG18 module for Modbus RTU (planned integration).

- **Software**
  - **Operating System:** Debian 12 (Bookworm)
  - **Backend:** Django Framework (Python)
  - **Database:** SQLite
  - **Frontend:** HTML, CSS, JavaScript
  - **APIs:** EVOK API for controlling relays, sensors, and inputs.

---

## 🚀 **Installation**

### Prerequisites
- Raspberry Pi running **Debian 12 (Bookworm)**.
- UniPi hardware connected with EMO-R8 module.
- DS18B20 sensors and Modbus RTU (xG18) connected.

### Step 1: Clone the Repository  
```bash
git clone https://github.com/jardahrazdera/fermentation_controller.git
cd fermentation_controller
```

### Step 2: Create a Virtual Environment  
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies  
```bash
pip install -r requirements.txt
```

### Step 4: Setup the Database  
```bash
python manage.py migrate
```

### Step 5: Run the Server  
```bash
python manage.py runserver
```

Access the web dashboard at: `http://localhost:8000`

---

## 📊 **Dashboard Preview**

The dashboard provides an overview of the system, including:
- Tank temperatures.
- Valve status.
- Chiller and pump control.
- Historical temperature trends.

*(Screenshots and UI previews will be added soon.)*

---

## 🛠️ **Future Enhancements**

- **Notifications and Alerts:** Email/SMS notifications for temperature deviations or faults.
- **Data Analytics:** Advanced visualizations and reporting.
- **Fault Simulation:** Test system behavior under simulated hardware failures.
- **Mobile Integration:** Responsive UI optimized for mobile devices.

---

## 🧑‍💻 **Contributing**

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description of changes.

---

## 📝 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🤝 **Contact**

**Author:** Jaroslav Hrazděra  
**GitHub:** [jardahrazdera](https://github.com/jardahrazdera)  
**Location:** Prušánky, Czech Republic  

For inquiries or collaborations, feel free to reach out!
