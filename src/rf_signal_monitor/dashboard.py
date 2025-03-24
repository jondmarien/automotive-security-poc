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
        self.duration = duration
        self.attack_probability = attack_probability
        self.threshold = threshold
        self.layout = Layout()
        self.detected_signals = []
        self.log_file = f"logs/rf_dashboard_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Initialize layout
        self._init_layout()
        self._init_tables()
    
    def _init_layout(self):
        """Initialize the dashboard layout"""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        self.layout["main"].split_row(
            Layout(name="signals", ratio=2),
            Layout(name="stats", ratio=1)
        )
        
        self.layout["signals"].split_column(
            Layout(name="current_signals"),
            Layout(name="historical")
        )
    
    def _init_tables(self):
        """Initialize the signal tables"""
        self.current_table = Table(
            title="Current RF Signals",
            box=ROUNDED,
            expand=True
        )
        self.current_table.add_column("Time", style="cyan")
        self.current_table.add_column("Frequency (MHz)", style="green")
        self.current_table.add_column("Strength (dBm)", style="magenta")
        self.current_table.add_column("Status", style="yellow")
        
        self.historical_table = Table(
            title="Signal History",
            box=ROUNDED,
            expand=True
        )
        self.historical_table.add_column("Time", style="cyan")
        self.historical_table.add_column("Frequency (MHz)", style="green")
        self.historical_table.add_column("Strength (dBm)", style="magenta")
        self.historical_table.add_column("Status", style="yellow")
    
    def _update_tables(self, signals):
        """Update the signal tables with new data"""
        # Clear current signals table
        self.current_table.rows.clear()
        
        # Update current signals (last 5)
        for signal in signals[-5:]:
            self.current_table.add_row(
                signal['time'],
                f"{signal['frequency']:.2f}",
                f"{signal['strength']:.2f}",
                signal['status']
            )
        
        # Update historical data (first 10)
        self.historical_table.rows.clear()
        for signal in signals[:10]:
            self.historical_table.add_row(
                signal['time'],
                f"{signal['frequency']:.2f}",
                f"{signal['strength']:.2f}",
                signal['status']
            )
    
    def _calculate_stats(self, signals):
        """Calculate signal statistics"""
        if not signals:
            return "No signals detected"
            
        total_signals = len(signals)
        suspicious_signals = len([s for s in signals if s['status'] == "SUSPICIOUS"])
        avg_strength = sum(s['strength'] for s in signals) / total_signals
        
        stats = f"""
        Total Signals: {total_signals}
        Suspicious Signals: {suspicious_signals}
        Average Signal Strength: {avg_strength:.2f} dBm
        Detection Threshold: {self.threshold} dBm
        """
        return stats
    
    def _log_signal(self, signal):
        """Log signal data to file"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(f"{signal['time']},{signal['frequency']},{signal['strength']},{signal['status']}\n")
    
    def update(self, frequency=None, strength=None):
        """Update the dashboard with new signal data"""
        if frequency is None:
            frequency = random.uniform(300, 3000)  # 300-3000 MHz
        if strength is None:
            strength = random.uniform(-90, -30)    # -90 to -30 dBm
        
        # Generate signal data
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        is_suspicious = (
            random.random() < self.attack_probability or
            strength > self.threshold
        )
        
        signal = {
            'time': current_time,
            'frequency': frequency,
            'strength': strength,
            'status': "SUSPICIOUS" if is_suspicious else "NORMAL"
        }
        
        # Add to detected signals and log
        self.detected_signals.append(signal)
        self._log_signal(signal)
        
        # Update display components
        self._update_tables(self.detected_signals)
        stats = self._calculate_stats(self.detected_signals)
        
        # Update layout
        self.layout["header"].update(
            Panel(
                Align.center("[bold]RF Signal Monitor Dashboard[/bold]"),
                style="bold white on blue"
            )
        )
        
        self.layout["current_signals"].update(self.current_table)
        self.layout["historical"].update(self.historical_table)
        self.layout["stats"].update(
            Panel(
                stats,
                title="Statistics",
                border_style="bright_blue"
            )
        )
        
        time_remaining = max(0, self.duration - len(self.detected_signals))
        self.layout["footer"].update(
            Panel(
                Align.center(f"Time Remaining: {time_remaining}s"),
                style="bold white on blue"
            )
        )
        
        return is_suspicious

def simulate_dashboard(duration=60, attack_probability=0.1):
    """
    Simulate the RF dashboard with generated data
    
    Args:
        duration (int): Duration of the simulation in seconds
        attack_probability (float): Probability of suspicious signals (0-1)
    """
    dashboard = RFDashboard(duration=duration, attack_probability=attack_probability)
    
    try:
        with Live(dashboard.layout, refresh_per_second=4) as live:
            for _ in range(duration):
                dashboard.update()
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("[yellow]Simulation stopped by user[/yellow]")

if __name__ == "__main__":
    # Run standalone simulation for 60 seconds with 10% attack probability
    simulate_dashboard(60, 0.1)
