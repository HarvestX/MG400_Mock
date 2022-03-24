from dobot_server import DobotServer

if __name__ == "__main__":

    required_socket_list = [
        [ '172.10.0.3', 29999 ],
        [ '172.10.0.3', 30003 ],
    ]

    for socket in required_socket_list:
        server = DobotServer(socket)
        server.start()
