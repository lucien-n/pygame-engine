from datetime import datetime


def log(*args) -> None:
    message = f"[{datetime.now().strftime('%X')}] "
    for arg in args:
        message += str(arg)
    print(message)
