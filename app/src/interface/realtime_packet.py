import numpy as np

RealtimePacketType = np.dtype([
    ('len', np.uint16,),
    ('reserve', np.uint16, (3, )),
    ('digital_input_bits', np.uint64,),
    ('digital_outputs', np.uint64,),
    ('robot_mode', np.uint64,),
    ('controller_timer', np.uint64,),
    ('run_time', np.uint64,),
    ('test_value', np.uint64,),
    ('safety_mode', np.float64,),
    ('speed_scaling', np.float64,),
    ('linear_momentum_norm', np.float64,),
    ('v_main', np.float64,),
    ('v_robot', np.float64,),
    ('i_robot', np.float64,),
    ('program_state', np.float64,),
    ('safety_status', np.float64,),
    ('tool_accelerometer_values', np.float64, (3, )),
    ('elbow_position', np.float64, (3, )),
    ('elbow_velocity', np.float64, (3, )),
    ('q_target', np.float64, (6, )),
    ('qd_target', np.float64, (6, )),
    ('qdd_target', np.float64, (6, )),
    ('i_target', np.float64, (6, )),
    ('m_target', np.float64, (6, )),
    ('q_actual', np.float64, (6, )),
    ('qd_actual', np.float64, (6, )),
    ('i_actual', np.float64, (6, )),
    ('i_control', np.float64, (6, )),
    ('tool_vector_actual', np.float64, (6, )),
    ('TCP_speed_actual', np.float64, (6, )),
    ('TCP_force', np.float64, (6, )),
    ('tool_vector_target', np.float64, (6, )),
    ('TCP_speed_target', np.float64, (6, )),
    ('motor_temperatures', np.float64, (6, )),
    ('joint_modes', np.float64, (6, )),
    ('v_actual', np.float64, (6, )),
    ('dummy', np.float64, (9, 6))])


class RealtimePacket:
    __contents = np.array([0], dtype=RealtimePacketType)

    def __init__(self) -> None:
        self.__contents['len'] = len(self.__contents.tobytes())

    def packet(self):
        self.print()
        return self.__contents.tobytes()

    def write(self, key: str, value):
        if not value in self.__contents:
            raise ValueError('Error has occurred in overwriting packet: ' + '"' + key + '"' + ' not found.')

        self.__contents[key] = value

    def print(self):
        print(self.__contents)
