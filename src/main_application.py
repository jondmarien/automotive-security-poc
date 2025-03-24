#!/usr/bin/env python3

import os
import sys
import time
import argparse
import threading
from rich.console import Console
from rich.prompt import Prompt

# Use absolute imports instead of relative imports
from integration.integrated_detector import IntegratedRFDetector
from dashboard import RFDashboard, simulate_dashboard

class AutoSecurityPOC:
    def __init__(self):
        self.console = Console()
        self.detector = IntegratedRFDetector()
        
    def display_welcome(self):
        self.console.print("\n" + "=" * 80)
        self.console.print("[bold blue]AUTOMOTIVE SECURITY POC - RF SIGNAL MONITOR[/bold blue]".center(80))
        self.console.print("[cyan]March 23, 2025[/cyan]".center(80))
        self.console.print("=" * 80 + "\n")
        
        self.console.print("[yellow]This application demonstrates the integration of OpenXC and HackRF One[/yellow]")
        self.console.print("[yellow]for detecting suspicious RF signals in the automotive security context.[/yellow]\n")
        
    def display_menu(self):
        self.console.print("[bold green]Available Options:[/bold green]")
        self.console.print("1. Run Integrated RF Detector")
        self.console.print("2. Show Dashboard (Simulation)")
        self.console.print("3. View Documentation")
        self.console.print("4. Exit\n")
        
    def run(self):
        self.display_welcome()
        
        while True:
            self.display_menu()
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                duration = int(Prompt.ask("Enter duration in seconds", default="60"))
                attack_prob = float(Prompt.ask("Enter attack probability (0-1)", default="0.1"))
                self.detector.run_integration(duration, attack_prob)
            
            elif choice == "2":
                self.console.print("[bold cyan]Starting Dashboard Simulation...[/bold cyan]")
                duration = int(Prompt.ask("Enter duration in seconds", default="60"))
                attack_prob = float(Prompt.ask("Enter attack probability (0-1)", default="0.1"))
                simulate_dashboard(duration=duration, attack_probability=attack_prob)
                
            elif choice == "3":
                self.console.print("\n[bold]Documentation Summary:[/bold]")
                self.console.print("- OpenXC Version: 3.1.4")
                self.console.print("- HackRF One: Used for RF signal detection")
                self.console.print("- Frequency Ranges: 315-433 MHz (key fobs), 13.56 MHz (NFC)")
                self.console.print("- Alert Threshold: -60 dBm")
                self.console.print("- Suspicious Signal Threshold: -45 dBm\n")
                Prompt.ask("Press Enter to continue")
                
            elif choice == "4":
                self.console.print("[bold red]Exiting application...[/bold red]")
                break

def main():
    """
    Main entry point for the application.
    Creates an instance of AutoSecurityPOC and calls its run() method.
    """
    app = AutoSecurityPOC()
    app.run()

if __name__ == "__main__":
    app = AutoSecurityPOC()
    app.run()
