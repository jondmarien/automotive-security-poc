def main():
    # Import here to avoid import errors
    import sys
    import os
       
    # Import your actual main function
    from rf_signal_monitor.main_application import main as app_main
    app_main()
       
if __name__ == "__main__":
    main()