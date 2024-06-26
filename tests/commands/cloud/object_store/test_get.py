# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import zipfile
from os import mkdir
from pathlib import Path
from unittest import mock

from click.testing import CliRunner

from lean.commands import lean
from lean.container import container
from tests.conftest import initialize_container


@mock.patch("zipfile.ZipFile")
def test_get_gets_value_when_key_is_given(mock_zipfile) -> None:
    archive = mock.Mock()
    mocked_read = mock.Mock()
    archive.return_value.read = mocked_read
    mock_zipfile.return_value.__enter__ = archive

    api_client = mock.Mock()
    api_client.is_authenticated.return_value = True
    initialize_container(api_client_to_use=api_client)

    result = CliRunner().invoke(lean, ["cloud", "object-store", "get", "test-key"])
    assert result.exit_code == 0
    container.api_client.object_store.get.assert_called_once_with(('test-key',), 'abc', container.logger)
