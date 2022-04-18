import struct

class RealtimePacket:

    # (value(int|double), bytes_count)
    contents = [
        (0, 2), # Message size
        [ (0, 2), (0, 2), (0, 2) ], # Reserved bits
        (0.0, 8), # Digital input bits
        (0.0, 8), # Digital outputs
        (0.0, 8), # Robot mode
        (0.0, 8), # Controller timer
        (0.0, 8), # Time
        (0.0, 8), # test_value
        (0.0, 8), # Safety mode
        (0.0, 8), # Speed scaling
        (0.0, 8), # Linear momentum norm
        (0.0, 8), # V main
        (0.0, 8), # V robot
        (0.0, 8), # I robot
        (0.0, 8), # Program state
        (0.0, 8), # Safety Status
        [ (0.0, 8), (0.0, 8), (0.0, 8) ], # Tool Accelerometer values
        [ (0.0, 8), (0.0, 8), (0.0, 8) ], # Elbow position
        [ (0.0, 8), (0.0, 8), (0.0, 8) ], # Elbow velocity
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # q target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # qd target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # qdd target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # I target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # M target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # q actual
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # qd actual
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # I actual
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # I control
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # Tool vector actual
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # TCP speed actual
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # TCP force
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # Tool vector target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # TCP speed target
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # Motor temperature
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # Joint modes
        [ (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8) ], # V actual
        [
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8),
            (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8), (0.0, 8)
        ], # Reserved bits
    ]

    __result: bytearray = None

    def packet(self):
        if self.__result is None:
            self.build()

        return self.__result

    def build(self):
        self.__result = self.__concat_contents(self.contents)

    def replace_contents(self, begin: int, end: int, value):
        if self.__result is None:
            self.build()

        expected_bytes_count = end - begin + 1
        if isinstance(value, float) and expected_bytes_count != 8 or\
            isinstance(value, int) and expected_bytes_count != 2:
                raise ValueError('Invalid replace segment or given value type')

        if isinstance(value, float):
            bytes_value = bytearray(struct.pack('<d', value))
        else:
            bytes_value = bytearray(value.to_bytes(2, 'big'))

        for i in range(0, expected_bytes_count):
            self.__result[begin + i] = bytes_value[i]


    def __concat_contents(self, contents):
        ret = bytearray()

        if isinstance(contents, tuple):
            (value, bytes_count) = contents
            if isinstance(value, float):
                return struct.pack('<d', value)

            return value.to_bytes(bytes_count, 'big')

        for item in contents:
            ret = bytearray(self.__concat_contents(item) + ret)

        return ret
