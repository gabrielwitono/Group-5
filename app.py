"""Hands-On 1 - minimal Flask app served on port 8000 for LAN access."""

import socket

from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home():
    """Send visitors straight to the Hands-On 1 page."""
    return redirect(url_for("hands_on_1"))


@app.route("/hands-on-1")
def hands_on_1():
    return render_template("hands-on-1.html")


def local_ips() -> list[str]:
    """Best-effort list of the non-loopback IPv4 addresses of this machine."""
    candidates: list[str] = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No packet is actually sent; this only asks the OS which interface
        # would be used for outbound traffic.
        sock.connect(("8.8.8.8", 80))
        candidates.append(sock.getsockname()[0])
    except OSError:
        pass
    finally:
        sock.close()

    try:
        candidates.extend(socket.gethostbyname_ex(socket.gethostname())[2])
    except OSError:
        pass

    unique: list[str] = []
    for ip in candidates:
        if ip.startswith("127.") or ip in unique:
            continue
        unique.append(ip)

    return unique or ["127.0.0.1"]


if __name__ == "__main__":
    host = "0.0.0.0"  # listen on every interface so other devices can connect
    port = 8000

    print("=" * 64)
    print("  Hands-On 1 - Flask app is starting")
    print(f"  On this machine:  http://127.0.0.1:{port}/hands-on-1")
    for ip in local_ips():
        print(f"  From the network: http://{ip}:{port}/hands-on-1")
    print("=" * 64)

    # debug on for helpful error pages; the auto-reloader is disabled so this
    # runs as a single process (easy to stop from the terminal).
    app.run(host=host, port=port, debug=True, use_reloader=False)
