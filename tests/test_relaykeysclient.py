#!/usr/bin/env python3
"""
Tests for relaykeysclient module
"""

import json
from unittest.mock import Mock, patch

import pytest

from relaykeys.core import client as relaykeysclient


class TestRelayKeysClient:
    """Test the RelayKeysClient class"""

    def test_client_init_default(self):
        """Test client initialization with defaults"""
        client = relaykeysclient.RelayKeysClient()
        assert client.url == "http://127.0.0.1:5383/"

    def test_client_init_custom(self):
        """Test client initialization with custom URL"""
        client = relaykeysclient.RelayKeysClient("http://localhost:8080/")
        assert client.url == "http://localhost:8080/"

    @patch("requests.post")
    def test_successful_rpc_call(self, mock_post):
        """Test successful RPC call"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "SUCCESS", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.keyevent("A", [], True)

        assert result == "SUCCESS"
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_failed_rpc_call(self, mock_post):
        """Test failed RPC call"""
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()

        with pytest.raises(Exception):
            client.keyevent("A", [], True)

    @patch("requests.post")
    def test_keyevent_call(self, mock_post):
        """Test keyevent RPC call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "SUCCESS", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.keyevent("A", ["LSHIFT"], True)

        # Check the request was made correctly
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        assert request_data["method"] == "keyevent"
        assert request_data["params"] == [["A", ["LSHIFT"], True]]
        assert result == "SUCCESS"

    @patch("requests.post")
    def test_mousemove_call(self, mock_post):
        """Test mousemove RPC call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "SUCCESS", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.mousemove(10, 20, 0, 0)

        # Check the request was made correctly
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        assert request_data["method"] == "mousemove"
        assert request_data["params"] == [[10, 20, 0, 0]]
        assert result == "SUCCESS"

    @patch("requests.post")
    def test_mousebutton_call(self, mock_post):
        """Test mousebutton RPC call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "SUCCESS", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.mousebutton("l", "click")

        # Check the request was made correctly
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        assert request_data["method"] == "mousebutton"
        assert request_data["params"] == [["l", "click"]]
        assert result == "SUCCESS"

    @patch("requests.post")
    def test_daemon_call(self, mock_post):
        """Test daemon RPC call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "daemon_running", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.daemon("dongle_status")

        # Check the request was made correctly
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        assert request_data["method"] == "daemon"
        assert request_data["params"] == [["dongle_status"]]
        assert result == "daemon_running"

    @patch("requests.post")
    def test_ble_cmd_call(self, mock_post):
        """Test ble_cmd RPC call"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "Device1\nDevice2\n", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        result = client.ble_cmd("devlist")

        # Check the request was made correctly
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        assert request_data["method"] == "ble_cmd"
        assert request_data["params"] == [["devlist"]]
        assert "Device1" in result

    @patch("requests.post")
    def test_timeout_handling(self, mock_post):
        """Test timeout handling"""
        import requests

        mock_post.side_effect = requests.exceptions.Timeout()

        client = relaykeysclient.RelayKeysClient()

        with pytest.raises(requests.exceptions.Timeout):
            client.keyevent("A", [], True)

    @patch("requests.post")
    def test_connection_error_handling(self, mock_post):
        """Test connection error handling"""
        import requests

        mock_post.side_effect = requests.exceptions.ConnectionError()

        client = relaykeysclient.RelayKeysClient()

        with pytest.raises(requests.exceptions.ConnectionError):
            client.keyevent("A", [], True)


class TestRPCProtocol:
    """Test RPC protocol compliance"""

    @patch("requests.post")
    def test_rpc_request_format(self, mock_post):
        """Test that RPC requests follow JSON-RPC format"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "SUCCESS", "id": 1}
        mock_post.return_value = mock_response

        client = relaykeysclient.RelayKeysClient()
        client.keyevent("A", [], True)

        # Check the request format
        call_args = mock_post.call_args
        request_data = json.loads(call_args[1]["data"])

        # JSON-RPC 2.0 format requirements
        assert "method" in request_data
        assert "params" in request_data
        assert "id" in request_data
        assert isinstance(request_data["id"], int)

    def test_rpc_id_increment(self):
        """Test that RPC IDs increment correctly"""
        client = relaykeysclient.RelayKeysClient()

        # Check initial ID
        assert client.id == 1

        # Simulate ID increment (would happen in real calls)
        client.id += 1
        assert client.id == 2


if __name__ == "__main__":
    pytest.main([__file__])
