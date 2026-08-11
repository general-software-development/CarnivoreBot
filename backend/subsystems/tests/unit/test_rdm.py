import pytest
import time

from subsystems.core import runtimeDataManager as RDM

async def clear_rdm_data(sub: str):
    await RDM.writeSubsystem(sub, {})

import random

class TestRead:
    async def prep_mock(self):
        RDM.data = {
            "cache": {
                "test": 123
            },
            "downloaded": {
                "model": "abc",
                "modelData": [ 1, 2, 3 ]
            }
        }

    @pytest.mark.parametrize(["subsystemName", "keyName", "expectedValue"], [
        ["cache", "test", 123],
        ["downloaded", "model", "abc"],
        ["downloaded", "modelData", [1, 2, 3]]
    ])
    async def test_eq_read_value(self, subsystemName: str, keyName: str, expectedValue):
        await self.prep_mock()

        data = await RDM.readData(subsystemName, keyName)

        assert data == expectedValue

    @pytest.mark.parametrize(["subsystemName", "keyName", "expectedValue", "expectedResult"], [
        ["cache", "test", 123, True],
        ["downloaded", "model", "abc", True],
        ["downloaded", "modelData", [1, 2, 3], False]
    ])
    async def test_is_read_value(self, subsystemName: str, keyName: str, expectedValue, expectedResult: bool):
        await self.prep_mock()

        data = await RDM.readData(subsystemName, keyName)

        assert (data is expectedValue) if expectedResult else (data is not expectedValue)

    @pytest.mark.parametrize(["subsystemName", "expectedDict"], [
        ["cache", { "test": 123 }],
        ["downloaded", { "model": "abc", "modelData": [1, 2, 3] }]
    ])
    async def test_eq_read_sub(self, subsystemName: str, expectedDict: dict):
        await self.prep_mock()

        data = await RDM.readSubsystem(subsystemName)

        assert data == expectedDict

    @pytest.mark.parametrize(["subsystemName", "expectedDict"], [
        ["cache", { "test": 123 }],
        ["downloaded", { "model": "abc", "modelData": [1, 2, 3] }]
    ])
    async def test_is_read_sub(self, subsystemName: str, expectedDict: dict):
        await self.prep_mock()

        data = await RDM.readSubsystem(subsystemName)

        assert data is not expectedDict

    async def test_read_missing(self):
        await self.prep_mock()

        data = await RDM.readData("fake", "missing")
        assert data is None

    async def test_read_sub_missing(self):
        await self.prep_mock()

        data = await RDM.readSubsystem("fake")
        assert data is None

class TestWriteRead:
    async def prep_mock(self):
        RDM.data = {
            "cache": {
                "test": 123
            },
            "downloaded": {
                "model": "abc",
                "modelData": [ 1, 2, 3 ]
            }
        }

    async def test_update_1(self):
        await self.prep_mock()

        original = await RDM.readData('cache', 'test')
        assert original == 123

        await RDM.writeData('cache', 'test', 124)
        new = await RDM.readData('cache', 'test')
        assert new == 124

    async def test_update_2(self):
        await self.prep_mock()

        original = await RDM.readData('downloaded', 'modelData')
        assert original == [1, 2, 3]
        original[1] = 3
        await RDM.writeData('downloaded', 'modelData', original)

        new = await RDM.readData('downloaded', 'modelData')
        assert new == [1, 3, 3]

        sub = await RDM.readSubsystem('downloaded')
        assert sub['modelData'] == [1, 3, 3]

    async def test_indifference_subsystem(self):
        await self.prep_mock()

        await RDM.writeData('cache', 'test', random.randint(0, 10000))

        assert (await RDM.readData('downloaded', 'model')) == "abc"

    async def test_indifference_key(self):
        await self.prep_mock()

        await RDM.writeData('downloaded', 'model', 'newModel')

        assert (await RDM.readData('downloaded', 'modelData')) == [1, 2, 3]

class TestDelay:
    async def prep_mock_template(self):
        RDM.data = {
            "cache": {
                "test": 123
            },
            "downloaded": {
                "model": "abc",
                "modelData": [ 1, 2, 3 ]
            }
        }

    async def prep_mock_empty(self):
        RDM.data = {}

    @pytest.mark.parametrize(["maxDelayMs"], [[100], [50], [10], [1]])
    async def test_write_key(self, maxDelayMs: int):
        await self.prep_mock_template()

        start = time.time()
        await RDM.writeData("cache", "test", 188)
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000

    @pytest.mark.parametrize(["maxDelayMs"], [[100], [50], [10], [1]])
    async def test_write_key_create_sub(self, maxDelayMs: int):
        await self.prep_mock_empty()

        start = time.time()
        await RDM.writeData("cache", "test", 188)
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000

    @pytest.mark.parametrize(["maxDelayMs"], [[100], [50], [10], [1]])
    async def test_write_key(self, maxDelayMs: int):
        await self.prep_mock_template()

        start = time.time()
        await RDM.writeSubsystem("cache", { "test": 188 } )
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000

    @pytest.mark.parametrize(["maxDelayMs"], [[100], [50], [10], [1]])
    async def test_write_key_create_sub(self, maxDelayMs: int):
        await self.prep_mock_template()

        start = time.time()
        await RDM.writeSubsystem("cache", { "test": 188 } )
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000

    @pytest.mark.parametrize(["maxDelayMs"], [[50], [10], [1]])
    async def test_read_key(self, maxDelayMs: int):
        await self.prep_mock_template()

        start = time.time()
        await RDM.readData("cache", "test")
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000

    @pytest.mark.parametrize(["maxDelayMs"], [[50], [10], [1]])
    async def test_read_sub(self, maxDelayMs: int):
        await self.prep_mock_template()

        start = time.time()
        await RDM.readSubsystem("cache")
        dt = time.time() - start

        assert dt <= maxDelayMs / 1000
