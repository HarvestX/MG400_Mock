"""RealtimePacket."""
# Copyright 2022 HarvestX Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

RealtimePacketType = np.dtype([
    ('len', np.uint16,),
    ('not_used_01', np.uint16, (3, )),
    ('digital_inputs', np.uint64,),
    ('digital_outputs', np.uint64,),
    ('robot_mode', np.uint64,),
    ('not_used_02', np.uint64,),
    ('not_used_03', np.uint64,),
    ('test_value', np.uint64,),
    ('not_used_04', np.float64,),
    ('speed_scaling', np.float64,),
    ('not_used_05', np.float64,),
    ('not_used_06', np.float64,),
    ('not_used_07', np.float64,),
    ('not_used_08', np.float64,),
    ('not_used_09', np.float64,),
    ('not_used_10', np.float64,),
    ('not_used_11', np.float64, (3, )),
    ('not_used_12', np.float64, (3, )),
    ('not_used_13', np.float64, (3, )),
    ('q_target', np.float64, (6, )),
    ('qd_target', np.float64, (6, )),
    ('qdd_target', np.float64, (6, )),
    ('i_target', np.float64, (6, )),
    ('m_target', np.float64, (6, )),
    ('q_actual', np.float64, (6, )),
    ('qd_actual', np.float64, (6, )),
    ('i_actual', np.float64, (6, )),
    ('actual_i_TCP_force', np.float64, (6, )),
    ('tool_vector_actual', np.float64, (6, )),
    ('TCP_speed_actual', np.float64, (6, )),
    ('TCP_force', np.float64, (6, )),
    ('tool_vector_target', np.float64, (6, )),
    ('TCP_speed_target', np.float64, (6, )),
    ('not_used_14', np.float64, (6, )),
    ('not_used_15', np.float64, (6, )),
    ('not_used_16', np.float64, (6, )),
    ('not_used_17', np.uint64, (14, )),  # HandType ~ Reserved 112/8 = 14
    ('not_used_18', np.float64, (6,)),
    ('load', np.float64,),
    ('center_x', np.float64,),
    ('center_y', np.float64,),
    ('center_z', np.float64,),
    ('not_used_19', np.float64, (6,)),  # User
    ('not_used_20', np.float64, (6,)),  # Tool
    ('not_used_21', np.float64,),  # TraceIndex
    ('not_used_22', np.float64, (6,)),  # FixForceValue
    ('not_used_23', np.float64, (4,)),  # Target Quaternion
    ('not_used_24', np.float64, (4,)),  # Actual Quaternion
    ('not_used_25', np.uint8, (24,)),  # Revered 24/8 = 3
])


class RealtimePacket:
    """RealtimePacket"""
    __contents = np.array([0], dtype=RealtimePacketType)

    def __init__(self) -> None:
        self.__contents['len'] = len(self.__contents.tobytes())

    def packet(self):
        """return the dobot status as a packet."""
        return self.__contents.tobytes()

    def write(self, key: str, value):
        """write the status to a packet."""
        self.__contents[key] = value

    def read(self, key: str):
        """read the status from the packet."""
        return self.__contents[key]
