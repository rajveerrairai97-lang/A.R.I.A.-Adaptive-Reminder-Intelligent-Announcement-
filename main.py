import threading
import time
import webbrowser

from dashboard import run_dashboard
from notifier import notify
from personality import generate_startup_message
from scheduler import start_scheduler


def open_browser():

    time.sleep(2)

    webbrowser.open(
        "http://127.0.0.1:5000"
    )


def main():

    print()

    print(
        "=" * 65
    )

    print(
        "🔷 JARVIS NOTIFICATION ENGINE V3"
    )

    print(
        "🇮🇳 India Standard Time"
    )

    print(
        "🌐 Browser dashboard: http://127.0.0.1:5000"
    )

    print(
        "=" * 65
    )


    start_scheduler()


    browser_thread = threading.Thread(
        target=open_browser,
        daemon=True
    )

    browser_thread.start()


    notify(
        generate_startup_message(),
        title="🔷 JARVIS ONLINE"
    )


    run_dashboard()


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n🔷 JARVIS shutting down, sir."
        )