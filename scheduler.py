import os
import subprocess
import sys
import time

import schedule
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class PdfFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        if event.src_path.endswith(".pdf"):
            run_main()


def run_email_fetch_test():
    script_path = os.path.join("email_tools", "email_fetch.py")
    subprocess.Popen([sys.executable, script_path])


def run_main():
    subprocess.Popen([sys.executable, "main.py"])


def watch_mail_pdfs_folder():
    path = "./mailPdfs"
    event_handler = PdfFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


schedule.every(10).seconds.do(run_email_fetch_test)

# Run the watchdog in a separate thread
import threading

thread = threading.Thread(target=watch_mail_pdfs_folder)
thread.daemon = True  # Set as daemon so it exits when main thread exits
thread.start()

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully...")
