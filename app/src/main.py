import interface

import logging
logging.basicConfig(level=logging.INFO)


def main():
    dashboard_tcp = interface.DashboardTcp('172.10.0.3', 29999)
    dashboard_tcp.start()

    motion_tcp = interface.MotionTcpInterface('172.10.0.3', 30003)
    motion_tcp.start()

    feedback_tcp = interface.RealtimeFeedbackTcpInterface('172.10.0.3', 30004)
    feedback_tcp.start()

if __name__ == "__main__":
    main()
