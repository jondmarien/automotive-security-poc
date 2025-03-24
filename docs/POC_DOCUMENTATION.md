
# Automotive Security POC - RF Signal Monitor

## Project Overview

The Automotive Security Proof of Concept (POC) is a comprehensive monitoring system designed to detect and alert on suspicious RF signals that could indicate potential security threats to modern vehicles. The system integrates the OpenXC platform with a HackRF One software-defined radio to provide real-time monitoring, detection, and alerting capabilities for automotive security professionals and researchers.

The POC specifically focuses on detecting anomalous RF signals in common automotive frequency ranges (primarily 315MHz and 433MHz) that could indicate attacks such as:
- Key fob relay attacks.
- Key cloning attempts.
- Signal jamming.
- Unauthorized transmissions.

This system demonstrates the practical implementation of a defensive monitoring solution that could be deployed in vehicles or parking facilities to enhance automotive cybersecurity.

## Installation and Setup Instructions

### Prerequisites

- Python 3.6 or higher.
- HackRF One or compatible SDR hardware.
- OpenXC Vehicle Interface (or simulator).
- Required Python packages:
    - `rich`
    - `pyserial` (for connection to physical devices)
    - `threading`

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/automotive-security-poc.git
   cd automotive-security-poc
   ```

2. **Set Up Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Hardware (If using physical devices)**
   - Connect HackRF One to your computer via USB
   - Ensure OpenXC Vehicle Interface is connected or the simulator is configured
   - Verify that all devices are recognized by your system

5. **Prepare Log Directories**

   ```bash
   mkdir -p src/logs/dashboard
   mkdir -p src/logs/integrated
   ```

## Usage Guide

### Running the Application

1. **Start the Main Application**

   ```bash
   cd src
   python main_application.py
   ```

2. **Main Menu Options**
   The application presents the following options:
   
   - **Run Integrated RF Detector**: Starts the real-time monitoring of RF signals with integrated OpenXC data
   - **Show Dashboard (Simulation)**: Launches the visualization dashboard with simulated data
   - **View Documentation**: Displays brief documentation about the system
   - **Exit**: Closes the application

### Using the RF Detector

When running the RF detector, you can configure:

- **Duration**: How long to run the detection (in seconds)
- **Attack Probability**: For simulation purposes, the likelihood of generating suspicious signals

The detector will display:

- OpenXC signals from the vehicle
- Detected RF signals and their strength
- Alerts when suspicious signals are detected

### Dashboard Visualization

The dashboard provides a comprehensive view of:

- Real-time RF signal monitoring
- Vehicle data from OpenXC
- Alert history
- System status

All detection sessions are logged to files in the logs directory for later analysis.

## Screenshots

The following screenshots demonstrate the application in action:

![Dashboard View](./app_mockups/dashboard%20v2.png)
*Main dashboard showing RF signal monitoring and vehicle status*

![Alerts Screen](./app_mockups/alerts%20screen%20v2.png)

*Alerts panel showing detected suspicious signals*

![Alert Details](./app_mockups/alert%20details%20v1.png)
*Detailed view of a specific alert*

![Detection History](./app_mockups/detection%20history%20v1.png)
*Historical log of detected signals*

![Monitoring Settings](./app_mockups/monitoring%20settings%20v4.png)
*Configuration settings for the monitoring system*

## Mobile App Mockups

The project includes a companion mobile application designed to provide alerts and monitoring capabilities on the go. The mobile app connects to the main system and provides users with real-time notifications of potential security threats.

Mockups for the mobile application are available in:

- Figma project file (contact project maintainer for access).
- PNG mockups in the `app_mockups` directory.

Key mobile app features include:

- Real-time alerts for suspicious RF activity.
- Vehicle status monitoring.
- Historical detection records.
- Customizable alert settings.
- Secure authentication.

![Sign-in Page](./app_mockups/sign-in%20page%20v1.png)
*Mobile app authentication screen*

## Future Development Recommendations

Based on the current state of the proof of concept, the following enhancements are recommended for future development:

### Short-term Improvements

1. **Enhanced Signal Analysis**
   - Implement machine learning algorithms to improve detection accuracy.
   - Add frequency spectrum visualization for better signal analysis.
   - Develop pattern recognition for known attack signatures.

2. **System Integration**
   - Create APIs for integration with existing vehicle security systems.
   - Develop plugins for popular automotive diagnostic tools.
   - Implement MQTT or other lightweight protocols for better IoT connectivity.

3. **User Interface Enhancements**
   - Add customizable dashboard widgets.
   - Improve alert categorization and prioritization.
   - Develop a more intuitive configuration interface.

### Long-term Vision

1. **Hardware Development**
   - Design a compact, dedicated hardware device for permanent installation.
   - Integrate with CAN bus for direct vehicle communication.
   - Develop low-power operation modes for extended monitoring.

2. **Cloud Integration**
   - Create a secure cloud platform for fleet monitoring.
   - Implement threat intelligence sharing between instances.
   - Develop a centralized database of known attack signatures.

3. **Advanced Features**
   - Automatic countermeasures for detected attacks.
   - GPS-based security zones with custom security policies.
   - Integration with smart home/parking facilities for comprehensive protection.

4. **Commercial Development**
   - Package as a consumer product for high-end vehicles.
   - Develop enterprise solutions for fleet operators and parking facilities.
   - Create OEM partnerships for factory installation options.

## Technical Architecture

The system consists of three main components:

1. **RF Signal Detection Module (HackRF)**
   - Monitors frequency bands commonly used in automotive systems.
   - Analyzes signal strength and patterns.
   - Identifies anomalous transmissions.

2. **Vehicle Integration Module (OpenXC)**
   - Collects real-time vehicle data.
   - Correlates vehicle events with RF activity.
   - Provides context for signal analysis.

3. **Monitoring and Alerting System**
   - Real-time dashboard visualization.
   - Alert generation and notification.
   - Historical data logging and analysis.

The system uses a modular architecture that allows components to be updated or replaced independently, facilitating ongoing development and improvement.

## Conclusion

The Automotive Security POC demonstrates a practical approach to monitoring and detecting potential RF-based attacks on modern vehicles. By combining software-defined radio technology with vehicle data integration, the system provides a comprehensive solution for automotive cybersecurity professionals.

This proof of concept serves as a foundation for more advanced security systems and highlights the importance of proactive monitoring in automotive security.

---

*Created: March 2025*