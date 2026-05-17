import itertools
import os
import sys
import threading
import time

from dataclasses import dataclass


@dataclass
class SpinnerThread:
    thread: threading.Thread
    event: threading.Event

    def stop(self) -> None:
        self.event.set()
        self.thread.join()


def _terminal_supports_colour() -> bool:
    return (
        os.environ.get("COLORTERM", "") == "truecolor"
        or os.environ.get("TERM", "") == "xterm-256color"
    )


def info(message: str) -> None:
    if _terminal_supports_colour():
        print(f"\033[1m[INFO]\033[0m: {message}")
        return

    print(f"[INFO]: {message}")


def ok(message: str) -> None:
    if _terminal_supports_colour():
        print(f"\033[1;32m[OK]\033[0m: {message}")
        return

    print(f"[OK]: {message}")


def error(message: str) -> None:
    if _terminal_supports_colour():
        print(f"\033[1;31m[ERROR]\033[0m: {message}")
        return

    print(f"[ERROR]: {message}")


def spinner() -> SpinnerThread:
    def spin(stopped: threading.Event) -> None:
        parts = itertools.cycle(["|", "/", "-", "\\"])

        while not stopped.is_set():
            sys.stdout.write(next(parts))
            sys.stdout.flush()
            time.sleep(0.175)
            sys.stdout.write("\b")

    signal_stop = threading.Event()
    thread = threading.Thread(target=spin, args=(signal_stop,))

    thread.start()

    return SpinnerThread(thread=thread, event=signal_stop)
