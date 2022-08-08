"""Return Msg Generator."""


def generate_return_msg(error_id: int, vals=None):
    """generate_return_msg"""
    if vals is None:
        vals = []
    msg = str(error_id) + ",{" + ",".join(map(str, vals)) + "},"
    return msg
