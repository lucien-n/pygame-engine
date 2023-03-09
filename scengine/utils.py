from datetime import datetime

debug = False


def log(*args) -> None:
    if not debug:
        return

    message = f"[{datetime.now().strftime('%X')}] "
    for arg in args:
        message += str(arg)
    print(message)
