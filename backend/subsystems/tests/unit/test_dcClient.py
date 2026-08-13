import pytest
from subsystems.core.dc.dcClient import isCommand

PREFIX = ';'

class TestIsCommand:
    @pytest.mark.parametrize(["commandName", "messageContent", "includePrefix", "expected"], [
        ["ping", ";ping", True, True],
        ["ping", ";getEnv", True, False],
        ["", "randomMessage", False, True],
        ["", ";command", True, True]
    ])
    def test_normal_usage(self, commandName: str, messageContent: str, includePrefix: bool, expected: bool):
        result = isCommand(messageContent, commandName, PREFIX if includePrefix else '')
        assert result == expected

    @pytest.mark.parametrize(["commandName", "messageContent", "includePrefix", "expected"], [
        ["ping", "ping", False, True],
        ["ping", "ping", True, False],
        ["ping", ";ping", False, False],
        ["", ";command", False, True]
    ])
    def test_prefixes(self, commandName: str, messageContent: str, includePrefix: bool, expected: bool):
        result = isCommand(messageContent, commandName, PREFIX if includePrefix else '')
        assert result == expected

    @pytest.mark.parametrize(["commandName", "messageContent", "includePrefix", "expected"], [
        ["ping", "getEnv", True, False],
        ["ping", "getEnv", False, False],
    ])
    def test_irrelevant_commands(self, commandName: str, messageContent: str, includePrefix: bool, expected: bool):
        result = isCommand(messageContent, commandName, PREFIX if includePrefix else '')
        assert result == expected

    @pytest.mark.parametrize(["commandName", "messageContent", "includePrefix", "expected"], [
        ["ping", ";pingSomething", True, False],
        ["ping", "pings", False, False]
    ])
    def test_longer_command(self, commandName: str, messageContent: str, includePrefix: bool, expected: bool):
        result = isCommand(messageContent, commandName, PREFIX if includePrefix else '')
        assert result == expected
