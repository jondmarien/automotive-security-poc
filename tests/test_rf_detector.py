import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Try to import the RFDetector class
try:
    from src.hackrf.rf_detector import RFDetector
    HAS_RF_DETECTOR = True
except ImportError:
    HAS_RF_DETECTOR = False

# Try to import GNURadio
try:
    import gnuradio
    HAS_GNURADIO = True
except ImportError:
    HAS_GNURADIO = False


# Skip all tests if RF detector module is not available
pytestmark = pytest.mark.skipif(
    not HAS_RF_DETECTOR,
    reason="RF detector module not available"
)


class TestRFDetector:
    """Test suite for RF detector functionality"""
    
    def test_initialization(self):
        """Test that the RF detector can be initialized with custom parameters"""
        detector = RFDetector(frequency_range=(315, 433), threshold=-70, duration=5)
        assert detector.frequency_range == (315, 433)
        assert detector.threshold == -70
        assert detector.duration == 5
    
    @patch('rich.live.Live')
    def test_detect_signals_simulation(self, mock_live):
        """Test the signal detection functionality in simulation mode"""
        # Configure the mock
        mock_live_instance = MagicMock()
        mock_live.return_value.__enter__.return_value = mock_live_instance
        
        # Create detector with short duration for testing
        detector = RFDetector(duration=0.5)
        
        # Run signal detection (simulation mode)
        detector.detect_signals()
        
        # Verify simulation was run (Live was used)
        mock_live.assert_called_once()
    
    @pytest.mark.skipif(not HAS_GNURADIO, reason="GNURadio not available")
    def test_gnuradio_features(self):
        """Test features that require GNURadio"""
        # This test will be skipped if GNURadio is not available
        detector = RFDetector()
        # Add assertions that test GNURadio-specific functionality
        assert hasattr(detector, 'gnuradio_available')
        assert detector.gnuradio_available == True
    
    def test_simulate_signal_detection(self):
        """Test the signal simulation functionality"""
        detector = RFDetector()
        # Test the internal simulation method
        signal = detector._simulate_signal_detection()
        # The result should be a boolean
        assert isinstance(signal, bool)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])

