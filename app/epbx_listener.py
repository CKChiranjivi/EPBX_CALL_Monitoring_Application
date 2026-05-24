import socket

EPBX_HOST = "10.0.32.11"
EPBX_PORT = 2300


def listen_epbx():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((EPBX_HOST, EPBX_PORT))

    print("Connected to EPBX")

    # login
    sock.send(b"smdr\n")
    sock.send(b"pccsmdr\n")

    while True:

        data = sock.recv(4096)

        if not data:
            continue

        print("RAW DATA:", repr(data))