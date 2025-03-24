#!/usr/bin/env python3

import time
import argparse
import threading
import random
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from datetime import datetime

# Use absolute imports instead of relative imports
from openxc.rf_simulator import RFDetector as OpenXCRFDetector
from hackrf.rf_detector import RFDetector as HackRFDetector

class IntegratedRFDetector:
    def __init__(self, threshold=-60):
        self.console = Console()
        self.threshold = threshold
        self.duration = 60  # Default value
        self.attack_probability = 0.1  # Default value
        self.detected_signals = []
        self.simulator_running = False
        self.detector_running = False
        self.log_file = f"../src/logs/integrated_detection_log_{time.strftime('%Y%m%d_%H%M%S')}.txt"
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
        self.simulator_table.add_column("Signal Strength (dBm)", style="yellow", justify="center")
        self.simulator_table.add_column("Type", style="magenta", justify="center")
        
        self.detector_table = Table(title="HackRF Signal Detection")
        self.detector_table.add_column("Timestamp", style="cyan", justify="center")
        self.detector_table.add_column("Frequency (MHz)", style="green", justify="center")
        self.detector_table.add_column("Signal Strength (dBm)", style="yellow", justify="center")
        self.detector_table.add_column("Status", style="bold red", justify="center")
    

    def _update_layout(self):
        """Update the layout with current data"""
        try:
            # Format the title with parameters
            title_params = f"[Duration: {self.duration} sec | Threshold: {self.threshold} dBm | Attack Prob: {int(self.attack_probability*100)}%]"
            header_content = Panel(
                f"[bold blue]Automotive Security POC - RF Signal Monitor [/bold blue][cyan]{title_params}[/cyan]",
                style="blue",
                title_align="center"
            )
            
            footer_content = Panel(
                f"[bold green]Log file: {self.log_file}[/bold green]",
                style="green",
                title_align="center"
            )
            
            self.layout["header"].update(header_content)
            
            # Use a simpler approach for the tables
            with self.table_lock:
                try:
                    # Check if the tables exist and have valid rows
                    if not hasattr(self, 'simulator_table') or self.simulator_table is None:
                        self._init_tables()
                    if not hasattr(self, 'detector_table') or self.detector_table is None:
                        self._init_tables()
                    
                    # Validate table structures
                    if not hasattr(self.simulator_table, 'rows') or not hasattr(self.detector_table, 'rows'):
                        self._init_tables()
                    
                    # Safely access table rows to prevent index errors
                    # Create panel only when tables are valid
                    simulator_panel = Panel(self.simulator_table, title="OpenXC Signal Simulator", title_align="center")
                    detector_panel = Panel(self.detector_table, title="HackRF Signal Detector", title_align="center")
                    
                    # Make sure we're working with valid tables before updating the layout
                    try:
                        self.layout["simulator"].update(simulator_panel)
                        self.layout["detector"].update(detector_panel)
                    except Exception as panel_error:
                        # If there's an error updating panels, log it but continue
                        print(f"Panel update error: {str(panel_error)}")
                except (IndexError, AttributeError) as idx_error:
                    # Specific handling for index errors in table manipulation
                    print(f"Table index error: {str(idx_error)}")
                    # Reinitialize tables if they're in an inconsistent state
                    self._init_tables()
                except Exception as table_error:
                    # Handle other table-related errors
                    print(f"Table error: {str(table_error)}")
            
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
            
            simple_layout["header"].update(Panel("RF Detection System - Error Recovery Mode", title_align="center"))
            simple_layout["body"].update(Panel(f"Processing data... Error: {str(e)}", title_align="center"))
            simple_layout["footer"].update(Panel(f"Log file: {self.log_file}", title_align="center"))
            
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
                
                # Determine frequency band (315 MHz or 433 MHz)
                freq_band = random.choice(["315", "433"])
                
                if is_attack:
                    # Generate more focused frequency ranges for attack signals
                    if freq_band == "315":
                        frequency = random.uniform(315.0, 316.0)
                    else:
                        frequency = random.uniform(433.0, 433.5)
                    signal_strength = random.uniform(-55, -40)
                    signal_type = "SUSPICIOUS"
                else:
                    # Generate wider frequency ranges for normal signals
                    if freq_band == "315":
                        frequency = random.uniform(314.0, 317.0)
                    else:
                        frequency = random.uniform(432.0, 434.0)
                    signal_strength = random.uniform(-80, -60)
                    signal_type = "Normal"
                
                # Log the generated signal
                log_entry = f"{timestamp} | {frequency:.1f} MHz | {signal_strength} dBm | {signal_type}\n"
                log.write(log_entry)
                log.flush()
                
                # Add to table (limited to 10 rows for display)
                with self.table_lock:
                    try:
                        if hasattr(self.simulator_table, 'rows') and self.simulator_table.rows:
                            if len(self.simulator_table.rows) >= 10:
                                self.simulator_table.rows.pop(0)
                            
                        self.simulator_table.add_row(
                            timestamp,
                            f"{frequency:.1f}",
                            f"{int(round(signal_strength))}",
                            f"[bold red]{signal_type}[/bold red]" if is_attack else signal_type
                        )
                    except Exception as e:
                        print(f"Error updating simulator table: {str(e)}")
                        # Attempt to recover by reinitializing the table
                        self._init_tables()
                
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
                try:
                    # Check if there are signals to process
                    signal = None
                    with self.table_lock:
                        if self.detected_signals and len(self.detected_signals) > 0:
                            try:
                                signal = self.detected_signals.pop(0)
                            except IndexError:
                                # Handle the case where another thread might have changed the list
                                signal = None
                        
                    if signal:
                        
                        # Simulate detection processing
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        frequency = signal['frequency']
                        signal_strength = signal['strength']
                        
                        # Determine if signal exceeds threshold
                        status = "Anomaly Detected!" if signal_strength > self.threshold else "Valid Signal"
                        
                        # Log the detected signal
                        log_entry = f"{timestamp} | {frequency:.1f} MHz | {signal_strength} dBm -> {status}\n"
                        log.write(log_entry)
                        log.flush()
                    
                        # Add to table (limited to 10 rows for display)
                        with self.table_lock:
                            try:
                                if hasattr(self.detector_table, 'rows') and self.detector_table.rows:
                                    if len(self.detector_table.rows) >= 10:
                                        self.detector_table.rows.pop(0)
                                    
                                self.detector_table.add_row(
                                    timestamp,
                                    f"{frequency:.1f}",
                                    f"{int(round(signal_strength))}",
                                    f"[bold red]{status}[/bold red]" if status == "Anomaly Detected!" else status
                                )
                            except Exception as e:
                                print(f"Error updating detector table: {str(e)}")
                                # Attempt to recover by reinitializing the table
                                self._init_tables()
                except Exception as e:
                    # Log the error but continue processing
                    log.write(f"Error processing signal: {str(e)}\n")
                    print(f"Signal processing error: {str(e)}")
                
                time.sleep(1)  # Detection processing interval
        
        self.detector_running = False
    
    def run_integration(self, duration=60, attack_probability=0.1):
        """Run the integration simulation for the specified duration"""
        print("Starting Integrated RF Detection System")
        # Store parameters as instance variables
        self.duration = duration
        self.attack_probability = attack_probability
        
        # Create log file with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.log_file = f"../src/logs/integrated_detection_log_{timestamp}.txt"
        
        with open(self.log_file, "w") as log:
            log.write("=== INTEGRATED RF DETECTION SYSTEM LOG ===\n")
            log.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Duration: {duration} seconds\n")
            log.write(f"Alert threshold: {self.threshold} dBm\n")
            log.write("-" * 50 + "\n")
            
            # Initialize threads
            self.simulator_running = True
            self.detector_running = True
            
            # Start threads
            simulator_thread = threading.Thread(target=self._simulator_thread, 
                                              args=(duration, attack_probability))
            detector_thread = threading.Thread(target=self._detector_thread, 
                                              args=(duration,))
            
            simulator_thread.start()
            detector_thread.start()
            
            # Alternative to Live display that doesn't cause thread issues
            try:
                start_time = time.time()
                console = Console()
                
                while time.time() - start_time < duration:
                    console.clear()
                    # Instead of using the complex Live widget, use simpler prints
                    try:
                        # Generate the layout once per iteration
                        layout = self._update_layout()
                        console.print(layout)
                    except IndexError as idx_err:
                        # Specifically handle index errors
                        console.print(f"Display error: {str(idx_err)}")
                        console.print(f"Processing data... Log file: {self.log_file}")
                        # Try to recover by reinitializing tables
                        with self.table_lock:
                            self._init_tables()
                    except Exception as e:
                        console.print(f"Display error: {str(e)}")
                        console.print(f"Processing data... Log file: {self.log_file}")
                                         # No need for constant refresh, sleep to reduce CPU usage
                    time.sleep(1)
                
                # Final display after completion
                try:
                    console.clear()
                    # Removed duplicate completion message - using the prettier one at the end
                except Exception as e:
                    # Ensure we don't crash during the final display
                    print(f"Final display error: {str(e)}")
                    # Removed duplicate completion message - using the prettier one at the end
                
            finally:
                # Stop threads and clean up
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
