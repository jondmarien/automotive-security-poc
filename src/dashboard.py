#!/usr/bin/env python3

import time
import random
import datetime
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED
from rich.align import Align

console = Console()

class RFDashboard:
    """Dashboard for RF Signal Monitoring in Automotive Security"""
    
    def __init__(self, duration=60, attack_probability=0.1, threshold=-60):
        """
        Initialize the dashboard
        
        Args:
            duration (int): Duration of the simulation in seconds
            attack_probability (float): Probability of generating a suspicious signal (0-1)
            threshold (int): Signal strength threshold in dBm for alerts
        """
        self.duration = duration
        self.attack_probability = attack_probability
        self.threshold = threshold
        self.signal_data = []
        # Add counters for total signals and alerts
        self.total_signals_detected = 0
        self.total_alerts_generated = 0
        
        # Define vehicle tags
        self.vehicle_tags = ["Vehicle 1", "Vehicle 2", "Vehicle 3"]
        
        # Create a dictionary of vehicle data with tags as keys
        self.vehicle_data = {}
        for tag in self.vehicle_tags:
            self.vehicle_data[tag] = {
                "Speed": "0 km/h", 
                "Door Status": "Closed", 
                "Engine Status": "Off",
                "Ignition": "Off",
                "Transmission": "Park",
                "Battery": "12.6V"
            }
        
        # Initialize with some sample alerts to make dashboard look realistic
        # Initialize with some sample alerts to make dashboard look realistic
        current_time = datetime.datetime.now()
        time_format = "%Y-%m-%d %H:%M:%S"
        self.alerts = [
            f"[{(current_time - datetime.timedelta(minutes=5)).strftime(time_format)}] [Vehicle 1] ALERT: Suspicious RF signal detected at 433.5 MHz (-42.3 dBm).",
            f"[{(current_time - datetime.timedelta(minutes=3)).strftime(time_format)}] [Vehicle 2] WARNING: Possible relay attack detected.",
            f"[{(current_time - datetime.timedelta(minutes=2)).strftime(time_format)}] [Vehicle 3] ALERT: Suspicious RF signal burst detected at 315.2 MHz.",
            f"[{(current_time - datetime.timedelta(minutes=1)).strftime(time_format)}] [Vehicle 1] WARNING: Key cloning attempt detected."
        ]
        
        # Initialize system status dictionary
        self.system_status = {
            "HackRF Connection": "✅ Connected",
            "OpenXC Simulation": "✅ Running",
            "Monitoring Active": "✅ Active",
            "Log Status": "✅ Recording"
        }
        self.start_time = datetime.datetime.now()
        self.start_timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        
        # Set log directory and create if it doesn't exist
        self.log_directory = "../src/logs/dashboard/"
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Set log filename with full path
        self.log_filename = f"{self.log_directory}dashboard_log_{self.start_timestamp}.txt"
        
        # Create initial log entry
        with open(self.log_filename, 'w') as log_file:
            log_file.write(f"======= RF SIGNAL MONITORING DASHBOARD LOG =======\n")
            log_file.write(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Duration: {self.duration} seconds\n")
            log_file.write(f"Attack Probability: {self.attack_probability}\n")
            log_file.write(f"Signal Threshold: {self.threshold} dBm\n")
            log_file.write("================================================\n\n")
        
    def generate_rf_signal(self):
        """Generate a simulated RF signal based on probability settings"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Randomly select a vehicle tag for this signal
        vehicle_tag = random.choice(self.vehicle_tags)
        
        # Determine if this will be a suspicious signal
        is_suspicious = random.random() < self.attack_probability
        
        # Generate frequency in common automotive bands (315MHz or 433MHz)
        frequency = random.choice([315, 433]) + random.random()
        
        # Signal strength depends on suspiciousness
        if is_suspicious:
            strength = random.uniform(-55, -40)  # Stronger signal if suspicious
            status = "SUSPICIOUS"
        else:
            strength = random.uniform(-80, -61)  # Normal range
            status = "Normal"
            
        # Create signal entry
        signal = {
            "timestamp": timestamp,
            "vehicle_tag": vehicle_tag,
            "frequency": round(frequency, 1),
            "strength": round(strength, 1),
            "status": status
        }
        
        # Add to signal data list (keep maximum 10 entries)
        # Add to signal data list (keep maximum 10 entries)
        self.signal_data.append(signal)
        # Increment total signals counter
        self.total_signals_detected += 1
        if len(self.signal_data) > 10:
            self.signal_data.pop(0)
            
        # Generate alert if suspicious
        if is_suspicious:
            alert_msg = f"[{timestamp}] [{signal['vehicle_tag']}] ALERT: Suspicious RF signal detected at {signal['frequency']} MHz ({signal['strength']} dBm)."
            self.alerts.append(alert_msg)
            # Increment total alerts counter
            self.total_alerts_generated += 1
            if len(self.alerts) > 10:
                self.alerts.pop(0)
        return signal
    
    def update_vehicle_data(self):
        """Update simulated vehicle data"""
        # Randomly change some vehicle parameters
        speed_values = ["0 km/h", "15 km/h", "35 km/h", "55 km/h", "70 km/h", "90 km/h"]
        door_values = ["Closed", "Driver Open", "Passenger Open", "All Closed"]
        engine_values = ["Running", "Running", "Running", "Off"]  # Weighted to mostly running
        ignition_values = ["On", "On", "On", "Off"]
        transmission_values = ["Park", "Drive", "Reverse", "Neutral"]
        battery_values = ["12.1V", "12.3V", "12.6V", "12.8V", "13.1V"]
        
        # Select a random vehicle to update
        vehicle_tag = random.choice(self.vehicle_tags)
        vehicle = self.vehicle_data[vehicle_tag]
        
        # Update the vehicle data
        vehicle["Speed"] = random.choice(speed_values)
        vehicle["Door Status"] = random.choice(door_values)
        vehicle["Engine Status"] = random.choice(engine_values)
        vehicle["Ignition"] = random.choice(ignition_values)
        vehicle["Transmission"] = random.choice(transmission_values)
        vehicle["Battery"] = random.choice(battery_values)
        
        # Generate vehicle-related alerts occasionally
        # Generate vehicle-related alerts occasionally
        if random.random() < 0.05:  # 5% chance for a vehicle alert
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert_types = [
                "Possible relay attack detected",
                "Key cloning attempt detected",
                "Suspicious RF signal burst detected",
                "RF jamming attempt detected",
                "Unknown RF transmitter detected in vicinity"
            ]
            alert_msg = f"[{timestamp}] [{vehicle_tag}] WARNING: {random.choice(alert_types)}."
            self.alerts.append(alert_msg)
            # Increment total alerts counter
            self.total_alerts_generated += 1
            if len(self.alerts) > 10:
                self.alerts.pop(0)
    def create_rf_table(self):
        """Create the RF Signal Monitoring table"""
        rf_table = Table(title="RF Signal Monitoring", box=ROUNDED)
        rf_table.add_column("Timestamp", style="cyan")
        rf_table.add_column("Vehicle", style="magenta")
        rf_table.add_column("Frequency (MHz)", style="green")
        rf_table.add_column("Signal Strength (dBm)", style="yellow")
        rf_table.add_column("Status", style="bold")
        
        for entry in self.signal_data:
            status_style = "[bold red]SUSPICIOUS[/bold red]" if entry["status"] == "SUSPICIOUS" else "Normal"
            rf_table.add_row(
                entry["timestamp"],
                entry["vehicle_tag"],
                f"{entry['frequency']:.1f}",
                f"{entry['strength']:.1f}",
                status_style
            )
            
        return rf_table
    
    def create_vehicle_table(self):
        """Create the Vehicle Data table with separate sections for each vehicle"""
        # Create a Table with title
        vehicle_table = Table(title="Vehicle Data by Tag", box=ROUNDED, padding=(0,1))
        
        # Add columns
        vehicle_table.add_column("Vehicle", style="magenta")
        vehicle_table.add_column("Parameter", style="cyan")
        vehicle_table.add_column("Value", style="green")
        
        # Add rows for each vehicle
        first_vehicle = True
        for vehicle_tag, data in self.vehicle_data.items():
            # Add separator between vehicles (except the first one)
            if not first_vehicle:
                vehicle_table.add_row("─────────", "─────────────", "────────────")
            else:
                first_vehicle = False
                
            # Add the first parameter with the vehicle tag
            first_param = list(data.keys())[0]
            vehicle_table.add_row(
                vehicle_tag, 
                first_param, 
                data[first_param]
            )
            
            # Add remaining parameters with empty vehicle tag cell
            items_list = list(data.items())
            for param, value in items_list[1:]:
                vehicle_table.add_row(
                    "", 
                    param, 
                    value
                )
        
        return vehicle_table
    
    def create_alerts_panel(self):
        """Create the Alerts panel"""
        if not self.alerts:
            content = "No active alerts"
        else:
            content = "\n".join(self.alerts)
            
        alerts_panel = Panel(
            content, 
            title="Alerts", 
            subtitle=f"[{len(self.alerts)} active]",
            border_style="red",
            box=ROUNDED
        )
        return alerts_panel
    
    def create_system_status_panel(self):
        """Create the System Status panel"""
        status_text = "\n".join([f"{k}: {v}" for k, v in self.system_status.items()])
        status_text += f"\nLog file: {self.log_filename}"
        
        system_panel = Panel(
            status_text,
            title="System Status",
            border_style="green",
            box=ROUNDED
        )
        return system_panel
    
    def log_data(self):
        """Write RF signal, vehicle data, and alerts to the log file"""
        with open(self.log_filename, 'a') as log_file:
            # Write timestamp
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"====== LOG ENTRY: {current_time} ======\n")
            
            # Write RF signal data
            log_file.write("RF SIGNALS:\n")
            for signal in self.signal_data:
                log_file.write(f"  {signal['timestamp']} | {signal['vehicle_tag']} | {signal['frequency']} MHz | {signal['strength']} dBm | {signal['status']}\n")
            
            # Write vehicle data
            # Write vehicle data
            log_file.write("\nVEHICLE DATA:\n")
            for vehicle_tag, data in self.vehicle_data.items():
                log_file.write(f"  {vehicle_tag}:\n")
                for param, value in data.items():
                    log_file.write(f"    {param}: {value}\n")
            log_file.write("\nALERTS:\n")
            for alert in self.alerts:
                log_file.write(f"  {alert}\n")
            
            log_file.write("\n")
    
    def create_header(self):
        """Create the dashboard header"""
        elapsed = (datetime.datetime.now() - self.start_time).seconds
        remaining = max(0, self.duration - elapsed)
        
        # Format elapsed and remaining time as MM:SS
        elapsed_min, elapsed_sec = divmod(elapsed, 60)
        remaining_min, remaining_sec = divmod(remaining, 60)
        elapsed_str = f"{elapsed_min:02d}:{elapsed_sec:02d}"
        remaining_str = f"{remaining_min:02d}:{remaining_sec:02d}"
        
        # Create header text with timer display
        header_text = (
            f"Automotive Security POC - RF Signal Monitor [Duration: {self.duration} sec | "
            f"Threshold: {self.threshold} dBm | Attack Prob: {int(self.attack_probability*100)}% | "
            f"Elapsed: [bold cyan]{elapsed_str}[/bold cyan] | Remaining: [bold yellow]{remaining_str}[/bold yellow]]"
        )
        
        # Create and return the header Panel
        header_panel = Panel(
            header_text,
            box=ROUNDED,
            border_style="blue"
        )
        return header_panel
    
    def create_dashboard(self):
        """Create the complete dashboard layout"""
        # Create the main layout
        layout = Layout()
        
        # Add header
        layout.split(
            Layout(self.create_header(), size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Split the body into two columns
        layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1)
        )
        
        # Split each column into two rows - give more space to vehicle data
        layout["left"].split(
            Layout(name="left_top", ratio=1),
            Layout(name="left_bottom", ratio=2)  # More space for vehicle data
        )
        
        layout["right"].split(
            Layout(name="right_top", ratio=2),  # More space for alerts
            Layout(name="right_bottom", ratio=1)
        )
        
        # Add RF monitoring table to top left
        layout["left_top"].update(Panel(
            self.create_rf_table(),
            title="OpenXC Signal Simulator",
            border_style="blue",
            box=ROUNDED
        ))
        
        # Add vehicle data table to bottom left - more space for vehicle data
        layout["left_bottom"].update(Panel(
            self.create_vehicle_table(),
            title="Vehicle Data",
            border_style="blue",
            box=ROUNDED
        ))
        
        # Add alerts panel to top right
        layout["right_top"].update(Panel(
            self.create_alerts_panel(),
            title="Alerts",
            border_style="red",
            box=ROUNDED
        ))
        
        # Add system status to bottom right
        layout["right_bottom"].update(Panel(
            self.create_system_status_panel(),
            title="HackRF Signal Detector",
            border_style="blue",
            box=ROUNDED
        ))
        
        # Add the footer with log information
        # Add the footer with log information
        layout["footer"].update(Panel(
            f"Log file: {self.log_filename}",
            box=ROUNDED
        ))
        return layout
    
    def run_dashboard(self, simulation=True):
        """Run the dashboard with live updates"""
        print(f"Starting RF Signal Monitoring Dashboard")
        
        try:
            with Live(self.create_dashboard(), refresh_per_second=1) as live:
                elapsed_time = 0
                while simulation and elapsed_time < self.duration:
                    # Generate new RF signal data
                    self.generate_rf_signal()
                    
                    # Update vehicle data
                    self.update_vehicle_data()
                    
                    # Log data to file
                    self.log_data()
                    # Update the live display
                    live.update(self.create_dashboard())
                    
                    # Sleep for a short time
                    time.sleep(2)
                    elapsed_time += 2
                    
                # Keep the final display if we exit the loop
                if not simulation:
                    while True:
                        # Generate new RF signal data
                        self.generate_rf_signal()
                        
                        # Update vehicle data
                        self.update_vehicle_data()
                        
                        # Log data to file
                        self.log_data()
                        
                        # Update the live display
                        live.update(self.create_dashboard())
                        
                        # Sleep for a short time
                        time.sleep(2)
        except KeyboardInterrupt:
            print("Dashboard stopped by user.")
        finally:
            # Write final log entry
            with open(self.log_filename, 'a') as log_file:
                end_time = datetime.datetime.now()
                duration = (end_time - self.start_time).total_seconds()
                log_file.write(f"\n======= SIMULATION COMPLETE =======\n")
                log_file.write(f"Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                log_file.write(f"Actual Duration: {duration:.1f} seconds\n")
                log_file.write(f"Total RF Signals Detected: {self.total_signals_detected}\n")
                log_file.write(f"Total Alerts Generated: {self.total_alerts_generated}\n")
                log_file.write("==================================\n")
            print(f"Processing data... Log file: {self.log_filename}")
    
def simulate_dashboard(duration=60, attack_probability=0.1):
    """
    Simulate the RF dashboard with generated data
    
    Args:
        duration (int): Duration of the simulation in seconds
        attack_probability (float): Probability of suspicious signals (0-1)
    """
    dashboard = RFDashboard(duration=duration, attack_probability=attack_probability)
    dashboard.run_dashboard(simulation=True)

if __name__ == "__main__":
    # Run standalone simulation for 60 seconds with 10% attack probability
    simulate_dashboard(60, 0.1)
