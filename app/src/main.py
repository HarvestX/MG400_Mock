import interface

import logging
logging.basicConfig(level=logging.INFO)


def main():
    realtime_tcp = interface.RealtimeTcp('172.10.0.3', 29999)
    realtime_tcp.start()

    dashboard_tcp = interface.DashboardTcp('172.10.0.3', 30003)
    dashboard_tcp.start()


if __name__ == "__main__":
    main()
