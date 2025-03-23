#!/usr/bin/env python3

import os
import time
import argparse
import numpy as np
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

class RFDetector:
    def __init__(self, frequency_range=(315, 433), threshold=-60, duration=60, cmd_args=None):
        self.frequency_range = frequency_range
        self.threshold = threshold
        self.duration = duration
        self.cmd_args = cmd_args  # Store the command line arguments
        self.console = Console()
        self.log_file = f"rf_detection_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        
        self.console.print(f"[bold green]RF Detector Initialized[/bold green]")
        self.console.print(f"Monitoring frequency range: {frequency_range[0]}-{frequency_range[1]} MHz")
        self.console.print(f"Alert threshold: {threshold} dBm")
        
    def start_hackrf_sweep(self, duration=60):
        """Start HackRF frequency sweep and return the process"""
        # For the POC, we'll simulate this by generating sample data
        self.console.print("[yellow]Starting HackRF sweep (simulated for POC)[/yellow]")
        return None
        
    def detect_signals(self, duration=60):
        """Detect RF signals from the HackRF One output"""
        # Update instance duration if provided
        if duration != 60:
            self.duration = duration
            
        self.console.print("\n[bold blue]Starting RF Signal Detection...[/bold blue]")
        
        # Store signal data for display
        signal_data = []
        max_rows = 10  # Maximum number of rows to display (increased from 5 to 10)
        
        start_time = time.time()
        
        # Open log file
        with open(self.log_file, "w") as log:
            log.write("Timestamp | Frequency (MHz) | Signal Strength (dBm) | Status\n")
            log.write("-" * 70 + "\n")
            
            # Use a simple loop without Live for more stability
            while time.time() - start_time < self.duration:
                # Simulate results (this would be replaced with actual HackRF data)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Randomly choose between normal and suspicious signals
                if np.random.random() < 0.1:  # 10% chance of suspicious signal
                    frequency = np.random.choice([315.7, 433.2])
                    signal_strength = np.random.uniform(-55, -30)
                    is_suspicious = True
                else:
                    frequency = np.random.choice([315.7, 433.2])
                    signal_strength = np.random.uniform(-80, -61)
                    is_suspicious = False
                
                # Determine if signal exceeds threshold
                status = "Anomaly Detected!" if signal_strength > self.threshold else "Valid Signal."
                
                # Format result for display and logging
                result = f"{timestamp} | {frequency:.1f} | {signal_strength:.1f} | {status}"
                log.write(result + "\n")
                log.flush()
                
                # Add to signal data, keeping only the most recent entries
                signal_data.append({
                    'timestamp': timestamp,
                    'frequency': frequency,
                    'strength': signal_strength,
                    'status': status,
                    'suspicious': is_suspicious
                })
                
                if len(signal_data) > max_rows:
                    signal_data = signal_data[-max_rows:]  # Keep only the most recent entries
                
                # Create a fresh table for each update
                table = Table(title="RF Signal Detection Results")
                table.add_column("Timestamp", style="cyan")
                table.add_column("Frequency (MHz)", style="green")
                table.add_column("Signal Strength (dBm)", style="yellow")
                table.add_column("Status", style="bold red")
                
                # Add all current data to the table
                for entry in signal_data:
                    table.add_row(
                        entry['timestamp'],
                        f"{entry['frequency']:.1f}",
                        f"{entry['strength']:.1f}",
                        "[bold red]ALERT[/bold red]" if entry['suspicious'] else "Normal"
                    )
                
                # THIS IS THE CRITICAL FIX:
                # Create layout after table is defined
                layout = Layout()
                
                # Here's the fixed panel content showing command line arguments
                cmd_args_display = " ".join(self.cmd_args) if self.cmd_args else "No arguments provided"
                
                layout.split(
                    Layout(Panel(
                        f"[bold green]RF Detector[/bold green]\n"
                        f"Command Line Arguments: {cmd_args_display}", 
                        title="Monitoring Parameters"), 
                        size=3),
                    Layout(table)
                )

                # Clear screen and print the layout
                os.system('cls' if os.name == 'nt' else 'clear')
                self.console.print(layout)
                
                # Sleep to simulate real-time processing
                time.sleep(np.random.uniform(0.5, 2.0))
        
        self.console.print(f"\n[bold green]Detection complete! Results saved to {self.log_file}[/bold green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and analyze RF signals with HackRF One")
    parser.add_argument("--duration", type=int, default=60, help="Duration of detection in seconds")
    parser.add_argument("--threshold", type=float, default=-60, help="Signal strength threshold in dBm")
    parser.add_argument("--freq-range", type=str, default="315,433", help="Frequency range to monitor (format: min,max)")
    args = parser.parse_args()
    
    # Parse frequency range
    freq_min, freq_max = map(int, args.freq_range.split(','))
    
    # Create detector with command line arguments
    detector = RFDetector(
        frequency_range=(freq_min, freq_max), 
        threshold=args.threshold, 
        duration=args.duration,
        cmd_args=sys.argv[1:]  # Store the original command line arguments
    )
    detector.detect_signals(args.duration)