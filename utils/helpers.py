import socket

def get_self_ip() -> str:
    """
    Utility to obtain the current user's own IP address.

    Starts a connection with a temporary socket and attempts to find its own IP.

    Returns
    -------
    str
        IP address of this client
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("1.1.1.1", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# a = get_self_ip()
# print(a)