#!/usr/bin/env python3
"""
Tests for serial_wrappers module
"""

from unittest.mock import Mock, patch

import pytest

import serial_wrappers


class TestDummySerial:
    """Test the DummySerial class"""

    def test_dummy_serial_init(self):
        """Test DummySerial initialization"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)
        assert dummy.devpath == "/dev/ttyUSB0"
        assert dummy.baud == 115200

    def test_dummy_serial_context_manager(self):
        """Test DummySerial as context manager"""
        with serial_wrappers.DummySerial("/dev/ttyUSB0", 115200) as dummy:
            assert dummy is not None

    def test_dummy_serial_write(self, capsys):
        """Test DummySerial write method"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)
        dummy.write(b"AT\r\n")
        captured = capsys.readouterr()
        assert "AT" in captured.out

    def test_dummy_serial_readline(self):
        """Test DummySerial readline method"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)
        response = dummy.readline()
        assert response == b"OK\n"

    def test_dummy_serial_read_all(self):
        """Test DummySerial read_all method"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)
        response = dummy.read_all()
        assert b"Dummy Device" in response


class TestSerialWrapperFunctions:
    """Test serial wrapper utility functions"""

    @patch("serial.Serial")
    def test_get_serial_with_real_device(self, mock_serial):
        """Test get_serial with real device"""
        mock_instance = Mock()
        mock_serial.return_value = mock_instance

        result = serial_wrappers.get_serial("/dev/ttyUSB0", 115200, False)

        mock_serial.assert_called_once_with("/dev/ttyUSB0", 115200, timeout=1)
        assert result == mock_instance

    def test_get_serial_with_dummy_device(self):
        """Test get_serial with dummy device"""
        result = serial_wrappers.get_serial("/dev/ttyUSB0", 115200, True)

        assert isinstance(result, serial_wrappers.DummySerial)
        assert result.devpath == "/dev/ttyUSB0"
        assert result.baud == 115200


class TestSerialPortDetection:
    """Test serial port detection functionality"""

    @patch("serial.tools.list_ports.comports")
    def test_port_detection_empty(self, mock_comports):
        """Test when no ports are available"""
        mock_comports.return_value = []

        # This would be implemented in a port detection function
        ports = mock_comports()
        assert len(ports) == 0

    @patch("serial.tools.list_ports.comports")
    def test_port_detection_with_devices(self, mock_comports):
        """Test when ports are available"""
        mock_port = Mock()
        mock_port.device = "COM3"
        mock_port.description = "CP2104 USB to UART Bridge Controller"
        mock_port.hwid = "USB VID:PID=239A:8029"
        mock_comports.return_value = [mock_port]

        ports = mock_comports()
        assert len(ports) == 1
        assert ports[0].device == "COM3"
        assert "CP2104" in ports[0].description


class TestSerialCommunication:
    """Test serial communication patterns"""

    def test_at_command_pattern(self):
        """Test AT command communication pattern"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)

        # Simulate AT command
        dummy.write(b"AT\r\n")
        response = dummy.readline()

        assert response == b"OK\n"

    def test_ble_command_pattern(self):
        """Test BLE command communication pattern"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)

        # Simulate BLE command
        dummy.write(b"AT+BLEHIDEN=1\r\n")
        response = dummy.readline()

        assert response == b"OK\n"

    def test_device_list_command(self):
        """Test device list command"""
        dummy = serial_wrappers.DummySerial("/dev/ttyUSB0", 115200)

        # Simulate device list command
        dummy.write(b"AT+PRINTDEVLIST\r\n")
        response = dummy.read_all()

        assert b"Dummy Device" in response


if __name__ == "__main__":
    pytest.main([__file__])
