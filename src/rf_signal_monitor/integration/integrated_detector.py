#!/usr/bin/env python3

import os
import time
import argparse
import threading
import subprocess
import random
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from datetime import datetime

# Use absolute imports instead of relative imports
from rf_signal_monitor.openxc.rf_simulator import RFDetector as OpenXCRFDetector
from rf_signal_monitor.hackrf.rf_detector import RFDetector as HackRFDetector

class IntegratedRFDetector:
    def __init__(self, threshold=-60):
        self.console = Console()
        self.threshold = threshold
        self.duration = 60  # Default value
        self.attack_probability = 0.1  # Default value
        self.detected_signals = []
        self.simulator_running = False
        self.detector_running = False
        self.log_file = f"logs/integrated_detection_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        self.table_lock = threading.Lock()
        
        # Initialize layout
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="simulator", ratio=1),
            Layout(name="detector", ratio=1)
        )
        
        # Initialize signal tables
        self._init_tables()
    
    def _init_tables(self):
        """Initialize or reinitialize the signal tables"""
        self.simulator_table = Table(title="OpenXC Signal Simulation")
        self.simulator_table.add_column("Timestamp", style="cyan", justify="center")
        self.simulator_table.add_column("Frequency (MHz)", style="green", justify="center")
        self.simulator_table.add_column("Signal Strength (dBm)", style="magenta", justify="center")
        self.simulator_table.add_column("Status", style="yellow", justify="center")
        
        self.detector_table = Table(title="HackRF Signal Detection")
        self.detector_table.add_column("Timestamp", style="cyan", justify="center")
        self.detector_table.add_column("Frequency (MHz)", style="green", justify="center")
        self.detector_table.add_column("Signal Strength (dBm)", style="magenta", justify="center")
        self.detector_table.add_column("Status", style="yellow", justify="center")

    def initialize(self):
        """Initialize both OpenXC and HackRF detectors"""
        try:
            self.openxc_detector = OpenXCRFDetector()
            self.hackrf_detector = HackRFDetector()
            return True
        except Exception as e:
            self.console.print(f"[bold red]Error initializing detectors: {str(e)}[/bold red]")
            return False

    def cleanup(self):
        """Clean up resources"""
        self.simulator_running = False
        self.detector_running = False
        if hasattr(self, 'openxc_detector'):
            self.openxc_detector.cleanup()
        if hasattr(self, 'hackrf_detector'):
            self.hackrf_detector.cleanup()

    def log_signal(self, timestamp, frequency, strength, status, source):
        """Log detected signals to file"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp},{frequency},{strength},{status},{source}\n")

    def update_tables(self, timestamp, frequency, strength, status, source):
        """Update the appropriate table with new signal data"""
        with self.table_lock:
            if source == "simulator":
                self.simulator_table.add_row(
                    timestamp,
                    f"{frequency:.2f}",
                    f"{strength:.2f}",
                    status
                )
            else:
                self.detector_table.add_row(
                    timestamp,
                    f"{frequency:.2f}",
                    f"{strength:.2f}",
                    status
                )

    def run_simulator(self):
        """Run the OpenXC signal simulator"""
        self.simulator_running = True
        while self.simulator_running:
            timestamp = datetime.now().strftime("%H:%M:%S")
            frequency = random.uniform(300, 3000)
            strength = random.uniform(-90, -30)
            
            # Simulate potential attack with probability
            is_attack = random.random() < self.attack_probability
            status = "ALERT!" if is_attack else "Normal"
            
            self.update_tables(timestamp, frequency, strength, status, "simulator")
            self.log_signal(timestamp, frequency, strength, status, "simulator")
            
            time.sleep(1)

    def run_detector(self):
        """Run the HackRF signal detector"""
        self.detector_running = True
        while self.detector_running:
            timestamp = datetime.now().strftime("%H:%M:%S")
            frequency = random.uniform(300, 3000)  # Replace with actual HackRF detection
            strength = random.uniform(-90, -30)    # Replace with actual signal strength
            
            # Determine if signal strength exceeds threshold
            status = "ALERT!" if strength > self.threshold else "Normal"
            
            self.update_tables(timestamp, frequency, strength, status, "detector")
            self.log_signal(timestamp, frequency, strength, status, "detector")
            
            time.sleep(1)

    def run(self, duration=None):
        """Run the integrated detection system"""
        if duration:
            self.duration = duration
            
        # Start simulator thread
        simulator_thread = threading.Thread(target=self.run_simulator)
        simulator_thread.daemon = True
        simulator_thread.start()
        
        # Start detector thread
        detector_thread = threading.Thread(target=self.run_detector)
        detector_thread.daemon = True
        detector_thread.start()
        
        try:
            with Live(self.layout, refresh_per_second=4) as live:
                start_time = time.time()
                while time.time() - start_time < self.duration:
                    # Update layout components
                    self.layout["header"].update(Panel("Integrated RF Detection System"))
                    self.layout["simulator"].update(self.simulator_table)
                    self.layout["detector"].update(self.detector_table)
                    self.layout["footer"].update(Panel(
                        f"Time Remaining: {int(self.duration - (time.time() - start_time))}s"
                    ))
                    time.sleep(0.25)
                    
        except KeyboardInterrupt:
            self.console.print("[yellow]Detection stopped by user[/yellow]")
        finally:
            self.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Integrated RF Detection System for Automotive Security")
    parser.add_argument("--duration", type=int, default=60, help="Duration of detection in seconds")
    parser.add_argument("--threshold", type=float, default=-60, help="Signal strength threshold in dBm")
    args = parser.parse_args()
    
    detector = IntegratedRFDetector(threshold=args.threshold)
    if detector.initialize():
        detector.run(duration=args.duration)
