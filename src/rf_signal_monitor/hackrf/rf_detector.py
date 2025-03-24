#!/usr/bin/env python3

import time
import sys
import argparse
import numpy as np
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
        self.cmd_args = cmd_args  # Store command-line arguments for display
        self.console = Console()
        self.log_file = f"logs/rf_detection_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        self.detected_signals = []
        
        # Initialize layout and tables
        self._init_display()
    
    def _init_display(self):
        """Initialize the display layout and tables"""
        self.layout = Layout()
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        self.signal_table = Table(title="Detected RF Signals")
        self.signal_table.add_column("Timestamp", style="cyan")
        self.signal_table.add_column("Frequency (MHz)", style="green")
        self.signal_table.add_column("Signal Strength (dBm)", style="magenta")
        self.signal_table.add_column("Status", style="yellow")
    
    def log_signal(self, timestamp, frequency, strength, status):
        """Log detected signals to file"""
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp},{frequency},{strength},{status}\n")
    
    def detect_signals(self):
        """Simulate signal detection with HackRF One"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        frequency = np.random.uniform(self.frequency_range[0], self.frequency_range[1])
        strength = np.random.uniform(-90, -30)
        status = "ALERT!" if strength > self.threshold else "Normal"
        
        self.detected_signals.append({
            'timestamp': timestamp,
            'frequency': frequency,
            'strength': strength,
            'status': status
        })
        
        self.log_signal(timestamp, frequency, strength, status)
        return timestamp, frequency, strength, status
    
    def update_display(self, signal_data):
        """Update the display with new signal data"""
        timestamp, frequency, strength, status = signal_data
        
        # Update signal table
        self.signal_table.add_row(
            timestamp,
            f"{frequency:.2f}",
            f"{strength:.2f}",
            status
        )
        
        # Update layout
        self.layout["header"].update(Panel("HackRF Signal Detection"))
        self.layout["main"].update(self.signal_table)
        self.layout["footer"].update(Panel(
            f"Monitoring {self.frequency_range[0]}-{self.frequency_range[1]} MHz | Threshold: {self.threshold} dBm"
        ))
    
    def run(self):
        """Run the RF detection system"""
        try:
            with Live(self.layout, refresh_per_second=4) as live:
                start_time = time.time()
                while time.time() - start_time < self.duration:
                    signal_data = self.detect_signals()
                    self.update_display(signal_data)
                    time.sleep(0.25)
        except KeyboardInterrupt:
            self.console.print("[yellow]Detection stopped by user[/yellow]")
    
    def cleanup(self):
        """Clean up resources"""
        pass  # Add cleanup code for actual HackRF device


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and analyze RF signals with HackRF One")
    parser.add_argument("--duration", type=int, default=60, help="Duration of detection in seconds")
    parser.add_argument("--threshold", type=float, default=-60, help="Signal strength threshold in dBm")
    parser.add_argument("--min-freq", type=int, default=315, help="Minimum frequency in MHz")
    parser.add_argument("--max-freq", type=int, default=433, help="Maximum frequency in MHz")
    args = parser.parse_args()
    
    detector = RFDetector(
        frequency_range=(args.min_freq, args.max_freq),
        threshold=args.threshold,
        duration=args.duration,
        cmd_args=args
    )
    detector.run()
