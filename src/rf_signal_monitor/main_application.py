#!/usr/bin/env python3

import os
import sys
import time
import argparse
import threading
from rich.console import Console
from rich.prompt import Prompt

# Use absolute imports instead of relative imports
from rf_signal_monitor.integration.integrated_detector import IntegratedRFDetector
# Handle Dashboard imports
try:
    from rf_signal_monitor.dashboard import RFDashboard, simulate_dashboard
except ImportError:
    # Fallback for development environment
    from .dashboard import RFDashboard, simulate_dashboard

class AutoSecurityPOC:
    def __init__(self):
        self.console = Console()
        self.detector = None
        self.dashboard = None
        self.simulation_thread = None
        self.running = False

    def initialize_detector(self):
        """Initialize the RF detector with appropriate settings."""
        self.detector = IntegratedRFDetector()
        return self.detector.initialize()

    def start_simulation(self):
        """Start the simulation in a separate thread."""
        if self.simulation_thread is None:
            self.simulation_thread = threading.Thread(target=simulate_dashboard, args=(self.dashboard,))
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

    def run(self):
        """Main application loop."""
        self.console.print("[bold green]Starting RF Signal Monitor...[/bold green]")
        
        if not self.initialize_detector():
            self.console.print("[bold red]Failed to initialize RF detector. Exiting...[/bold red]")
            return

        self.dashboard = RFDashboard()
        self.start_simulation()
        
        self.running = True
        try:
            while self.running:
                # Main application loop
                time.sleep(0.1)  # Prevent CPU overuse
                
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Shutting down...[/bold yellow]")
        finally:
            if self.detector:
                self.detector.cleanup()

def main():
    """
    Main entry point for the application.
    Creates an instance of AutoSecurityPOC and calls its run() method.
    """
    app = AutoSecurityPOC()
    app.run()

if __name__ == "__main__":
    main()
