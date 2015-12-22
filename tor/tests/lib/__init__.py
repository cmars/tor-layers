import socket
import time


def assert_connect(host, port):
    for i in range(60):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                return
            except ConnectionRefusedError: pass
        time.sleep(1)
    raise Exception("failed to connect")

