import numpy as np

RealtimePacketType = np.dtype([
    ('len', np.uint16,),
    ('reserved1', np.uint16, (3, )),
    ('digital_input_bits', np.uint64,),
    ('digital_outputs', np.uint64,),
    ('robot_mode', np.uint64,),
    ('notused1', np.uint64,),
    ('reserved2', np.uint64,),
    ('test_value', np.uint64,),
    ('reserved3', np.float64,),
    ('speed_scaling', np.float64,),
    ('notused2', np.float64,),
    ('notused3', np.float64,),
    ('notused4', np.float64,),
    ('notused5', np.float64,),
    ('reserved4', np.float64,),
    ('reserved5', np.float64,),
    ('notused6', np.float64, (3, )),
    ('notused7', np.float64, (3, )),
    ('notused8', np.float64, (3, )),
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
    ('notused9', np.float64, (6, )),
    ('notused10', np.float64, (6, )),
    ('notused11', np.float64, (6, )),
    ('notused12', np.float64, (4,)),
    ('notused13', np.uint8, (26, )),
    ('reserved6', np.uint8, (82, )),
    ('notused14', np.float64, (6,)),
    ('load', np.float64,),
    ('center_x', np.float64,),
    ('center_y', np.float64,),
    ('center_z', np.float64,),
    ('notused15', np.float64, (6,)),
    ('notused16', np.float64, (6,)),
    ('notused17', np.float64,),
    ('notused18', np.float64, (6,)),
    ('notused19', np.float64, (4,)),
    ('notused20', np.float64, (4,)),
    ('reserved7', np.uint8, (24,)),
    ])


class RealtimePacket:
    __contents = np.array([0], dtype=RealtimePacketType)

    def __init__(self) -> None:
        self.__contents['len'] = len(self.__contents.tobytes())

    def packet(self):
        return self.__contents.tobytes()

    def write(self, key: str, value):
        self.__contents[key] = value
