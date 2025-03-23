#!/usr/bin/env python3

import os
import time
import argparse
import threading
import subprocess
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from datetime import datetime

# Import our custom modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.openxc.rf_simulator import RFDetector as OpenXCRFDetector
from src.hackrf.rf_detector import RFDetector as HackRFDetector

class IntegratedRFDetector:
    def __init__(self, threshold=-60):
        self.console = Console()
        self.threshold = threshold
        self.detected_signals = []
        self.simulator_running = False
        self.detector_running = False
        self.log_file = f"integrated_detection_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
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
        self.simulator_table = Table(title="OpenXC Signal Simulation")
        self.simulator_table.add_column("Timestamp", style="cyan")
        self.simulator_table.add_column("Frequency (MHz)", style="green")
        self.simulator_table.add_column("Signal Strength (dBm)", style="yellow")
        self.simulator_table.add_column("Type", style="magenta")
        
        self.detector_table = Table(title="HackRF Signal Detection")
        self.detector_table.add_column("Timestamp", style="cyan")
        self.detector_table.add_column("Frequency (MHz)", style="green")
        self.detector_table.add_column("Signal Strength (dBm)", style="yellow")
        self.detector_table.add_column("Status", style="bold red")
    

    def _update_layout(self):
        """Update the layout with current data"""
        try:
            header_content = Panel(
                f"[bold blue]Automotive Security POC - RF Signal Monitor[/bold blue]",
                style="blue"
            )
            
            footer_content = Panel(
                f"[bold green]Log file: {self.log_file}[/bold green]",
                style="green"
            )
            
            self.layout["header"].update(header_content)
            
            # Use a simpler approach for the tables
            with self.table_lock:
                # Instead of copying the table, we'll directly use the tables
                # but we'll keep the lock during the whole update to prevent race conditions
                simulator_panel = Panel(self.simulator_table, title="OpenXC Signal Simulator")
                detector_panel = Panel(self.detector_table, title="HackRF Signal Detector")
                
                self.layout["simulator"].update(simulator_panel)
                self.layout["detector"].update(detector_panel)
            
            self.layout["footer"].update(footer_content)
            
            return self.layout
        
        except Exception as e:
            # Return a simple layout in case of error
            simple_layout = Layout()
            simple_layout.split(
                Layout(name="header", size=3),
                Layout(name="body", ratio=1),
                Layout(name="footer", size=3)
            )
            
            simple_layout["header"].update(Panel("RF Detection System - Error Recovery Mode"))
            simple_layout["body"].update(Panel(f"Processing data... Error: {str(e)}"))
            simple_layout["footer"].update(Panel(f"Log file: {self.log_file}"))
            
            return simple_layout
    
    def _simulator_thread(self, duration, attack_probability):
        """Thread function for simulating RF signals using OpenXC"""
        self.simulator_running = True
        
        with open(self.log_file, "a") as log:
            log.write("\n=== SIMULATION LOG ===\n")
            
            start_time = time.time()
            while self.simulator_running and time.time() - start_time < duration:
                # Simulate signal generation
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                is_attack = attack_probability > 0.5  # Simplified for demonstration
                
                if is_attack:
                    frequency = 433.2 if int(time.time()) % 2 == 0 else 315.7
                    signal_strength = -45
                    signal_type = "SUSPICIOUS"
                else:
                    frequency = 315.7 if int(time.time()) % 2 == 0 else 433.2
                    signal_strength = -70
                    signal_type = "Normal"
                
                # Log the generated signal
                log_entry = f"{timestamp} | {frequency:.1f} MHz | {signal_strength} dBm | {signal_type}\n"
                log.write(log_entry)
                log.flush()
                
                # Add to table (limited to 10 rows for display)
                with self.table_lock:
                    if len(self.simulator_table.rows) >= 10:
                        self.simulator_table.rows.pop(0)
                        
                    self.simulator_table.add_row(
                        timestamp,
                        f"{frequency:.1f}",
                        f"{signal_strength}",
                        f"[bold red]{signal_type}[/bold red]" if is_attack else signal_type
                    )
                
                # Send to detection thread via shared data structure
                with self.table_lock:
                    self.detected_signals.append({
                        'timestamp': timestamp,
                        'frequency': frequency,
                        'strength': signal_strength,
                        'type': signal_type
                    })
                
                time.sleep(2)  # Simulate data generation interval
        
        self.simulator_running = False
    def _detector_thread(self, duration):
        """Thread function for detecting RF signals using HackRF"""
        self.detector_running = True
        
        with open(self.log_file, "a") as log:
            log.write("\n=== DETECTION LOG ===\n")
            
            # Process signals with 1-second delay to simulate detection
            start_time = time.time()
            
            while self.detector_running and time.time() - start_time < duration:
                # Check if there are signals to process
                signal = None
                with self.table_lock:
                    if self.detected_signals:
                        signal = self.detected_signals.pop(0)
                        
                if signal:
                    
                    # Simulate detection processing
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    frequency = signal['frequency']
                    signal_strength = signal['strength']
                    
                    # Determine if signal exceeds threshold
                    status = "Anomaly Detected!" if signal_strength > self.threshold else "Valid Signal"
                    
                    # Log the detected signal
                    log_entry = f"{timestamp} | {frequency:.1f} MHz | {signal_strength} dBm → {status}\n"
                    log.write(log_entry)
                    log.flush()
                    
                    # Add to table (limited to 10 rows for display)
                    with self.table_lock:
                        if len(self.detector_table.rows) >= 10:
                            self.detector_table.rows.pop(0)
                            
                        self.detector_table.add_row(
                            timestamp,
                            f"{frequency:.1f}",
                            f"{signal_strength}",
                            f"[bold red]{status}[/bold red]" if status == "Anomaly Detected!" else status
                        )
                
                time.sleep(1)  # Detection processing interval
        
        self.detector_running = False
    
    def run_integration(self, duration=60, attack_probability=0.1):
        """Run the integrated RF detection system"""
        self.console.print("[bold green]Starting Integrated RF Detection System[/bold green]")
        
        # Initialize log file
        with open(self.log_file, "w") as log:
            log.write("=== INTEGRATED RF DETECTION SYSTEM LOG ===\n")
            log.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Duration: {duration} seconds\n")
            log.write(f"Alert threshold: {self.threshold} dBm\n")
            log.write("-" * 50 + "\n")
        
        # Start simulator and detector threads
        simulator_thread = threading.Thread(
            target=self._simulator_thread,
            args=(duration, attack_probability)
        )
        
        detector_thread = threading.Thread(
            target=self._detector_thread,
            args=(duration,)
        )
        
        simulator_thread.start()
        detector_thread.start()
        
        # Update display in real-time
        try:
            with Live(self._update_layout(), refresh_per_second=1) as live:
                start_time = time.time()
                
                while time.time() - start_time < duration:
                    live.update(self._update_layout())
                    time.sleep(0.5)
        finally:
            # Signal threads to stop and wait for them
            self.simulator_running = False
            self.detector_running = False
            simulator_thread.join()
            detector_thread.join()
        
        self.console.print(f"[bold green]Integration complete! Results saved to {self.log_file}[/bold green]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Integrated RF Detection System for Automotive Security")
    parser.add_argument("--duration", type=int, default=60, help="Duration of detection in seconds")
    parser.add_argument("--threshold", type=float, default=-60, help="Signal strength threshold in dBm")
    parser.add_argument("--attack-prob", type=float, default=0.1, help="Probability of attack signals (0-1)")
    args = parser.parse_args()
    
    integrated_system = IntegratedRFDetector(threshold=args.threshold)
    integrated_system.run_integration(args.duration, args.attack_prob)
