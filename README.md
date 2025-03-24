# Automotive Security POC - RF Signal Monitor

## Overview

The Automotive Security Proof of Concept (POC) is a monitoring system designed to detect and alert on suspicious RF signals that could indicate potential security threats to modern vehicles. It integrates the OpenXC platform with a HackRF One software-defined radio to provide real-time monitoring, detection, and alerting capabilities.

### Key Features

- Detection of anomalous RF signals in automotive frequency ranges (315MHz and 433MHz)
- Real-time monitoring dashboard with comprehensive visualization
- Alert system for suspicious activity (key fob relay attacks, cloning attempts, signal jamming)
- Integration with vehicle data through OpenXC
- Historical logging and analysis capabilities
- Mobile companion app for on-the-go monitoring and alerts

## Installation

### Prerequisites

- Python 3.6 or higher
- HackRF One or compatible SDR hardware
- OpenXC Vehicle Interface (or simulator)

### Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jondmarien/automotive-security-poc.git
   cd automotive-security-poc
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Log Directories**
   ```bash
   mkdir -p src/logs/dashboard
   mkdir -p src/logs/integrated
   ```

5. **Configure Hardware (If using physical devices)**
   - Connect HackRF One to your computer via USB
   - Ensure OpenXC Vehicle Interface is connected or simulator is configured

## Usage

1. **Start the Application**
   ```bash
   cd src
   python main_application.py
   ```

2. **Main Menu Options**
   - Run Integrated RF Detector: Starts real-time monitoring
   - Show Dashboard: Launches visualization dashboard
   - View Documentation: Displays system documentation
   - Exit: Closes the application

3. **Using the RF Detector**
   - Configure monitoring duration and detection parameters
   - View real-time RF signals and vehicle data
   - Receive alerts for suspicious activities

## Screenshots

The application includes several visualization screens:
- Main dashboard for RF signal monitoring
- Alert management interface
- Detection history logs
- Configuration settings

See the `app_mockups` directory for visual references.

## Technical Architecture

The system consists of three main components:

1. **RF Signal Detection Module (HackRF)**: Monitors frequency bands used in automotive systems
2. **Vehicle Integration Module (OpenXC)**: Collects real-time vehicle data
3. **Monitoring and Alerting System**: Provides dashboard visualization and alert generation

## Future Development

Planned enhancements include:
- Enhanced signal analysis with machine learning
- Integration with existing vehicle security systems
- Dedicated hardware development
- Cloud-based fleet monitoring
- Automatic countermeasures for detected attacks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that allows reuse of the code while requiring attribution to the original author. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that you include the original copyright notice and permission notice in all copies or substantial portions of the software.

---

For detailed documentation, please refer to the [POC Documentation](docs/POC_DOCUMENTATION.md).

