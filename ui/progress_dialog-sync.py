#!/usr/bin/env python
"""
Example of a synchronous progress bar dialog.
"""

import os
import time
from prompt_toolkit.shortcuts import progress_dialog


def worker(set_percentage, log_text):
    """
    This work function is called by `progress_dialog`. It runs in a
    background thread.

    The `set_percentage` function updates the progress bar, while
    log_text logs messages in the window.
    """
    percentage = 0
    for dirpath, dirnames, filenames in os.walk("../.."):
        for f in filenames:
            log_text(f"{dirpath} / {f}\n")
            set_percentage(percentage)
            percentage += 2
            time.sleep(0.1)

            if percentage >= 100:
                break
        if percentage >= 100:
            break

    # Show 100% for a second before quitting
    set_percentage(100)
    time.sleep(1)


def main():
    progress_dialog(
        title="Progress dialog example",
        text="As an example, we walk through the filesystem and print all directories",
        run_callback=worker,
    ).run()  # ✅ Synchronous run


if __name__ == "__main__":
    main()
