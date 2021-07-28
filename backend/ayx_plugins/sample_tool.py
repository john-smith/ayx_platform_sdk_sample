# Copyright (C) 2021 Alteryx, Inc. All rights reserved.
#
# Licensed under the ALTERYX SDK AND API LICENSE AGREEMENT;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.alteryx.com/alteryx-sdk-and-api-license-agreement
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example pass through tool."""
from ayx_python_sdk.core import (
    InputConnectionBase,
    Plugin,
    ProviderBase,
    register_plugin,
    RecordPacket,
    FieldType
)


class sample_tool(Plugin):
    def __init__(self, provider: ProviderBase):
        self.name = "Add new column"
        self.provider = provider
        self.output_anchor = self.provider.get_output_anchor("Output")

        self.provider.io.info(f"{self.name} tool started")
        self.name = provider.tool_config['new_column']

    def on_input_connection_opened(self, input_connection: InputConnectionBase) -> None:
        if input_connection.metadata is None:
            raise RuntimeError("Metadata must be set before setting containers.")

        input_connection.max_packet_size = 1000
        self.output_metadata = input_connection.metadata.clone()
        self.output_metadata.add_field("new_column", FieldType.v_wstring, size=65535)
        self.output_anchor.open(self.output_metadata)

    def on_record_packet(self, input_connection: InputConnectionBase) -> None:
        packet = input_connection.read()
        df = packet.to_dataframe()
        df['new_column'] = self.name
        self.output_anchor.write(
            RecordPacket.from_dataframe(
                self.output_metadata,
                df
            ))

    def on_complete(self) -> None:
        self.provider.io.info(f"{self.name} tool done")

AyxPlugin = register_plugin(sample_tool)
