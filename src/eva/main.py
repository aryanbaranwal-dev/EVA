
from datetime import datetime
from urllib.parse import quote_plus
import time
import platform
import os
import subprocess
import shutil
import webbrowser


ASSISTANT_NAME = "EVA"
USER_NAME = "Aryan"


# ==========================================
# APPROVED APPLICATIONS
# ==========================================

APP_ALLOWLIST = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "vscode": "vscode",
    "chrome": "chrome",
}


# ==========================================
# APPROVED WEBSITES
# ==========================================

WEBSITE_ALLOWLIST = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "linkedin": "https://www.linkedin.com",
}


# ==========================================
# APPROVED FOLDERS
# ==========================================

USER_HOME = os.path.expanduser("~")

EVA_PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

FOLDER_ALLOWLIST = {
    "desktop": os.path.join(USER_HOME, "Desktop"),
    "documents": os.path.join(USER_HOME, "Documents"),
    "downloads": os.path.join(USER_HOME, "Downloads"),
    "eva": EVA_PROJECT_PATH,
}


# ==========================================
# GREETING AND HELP
# ==========================================

def show_greeting():
    """Display EVA's welcome message."""

    print("=" * 40)
    print(f"       Welcome to {ASSISTANT_NAME}")
    print("=" * 40)

    print(f"Hello, {USER_NAME}!")
    print("EVA is ready to assist you.")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to close EVA.")


def show_help():
    """Display the list of available commands."""

    print(f"\n{ASSISTANT_NAME}: Available commands:")

    print("  help                - Show available commands")
    print("  what can you do?    - Show my capabilities")
    print("  time                - Show the current time")
    print("  date                - Show today's date")
    print("  timer <seconds>     - Start a timer")
    print("  system              - Show system information")
    print("  open <app>          - Open an approved application")
    print("  website <name>      - Open an approved website")
    print("  folder <name>       - Open an approved folder")
    print("  search <query>      - Search Google")
    print("  exit                - Close EVA")


def show_capabilities():
    """Explain what EVA can currently do."""

    print(f"\n{ASSISTANT_NAME}: Currently, I can:")

    print("- Display the current date and time.")
    print("- Explain my available commands.")
    print("- Run a simple countdown timer.")
    print("- Display basic system information.")
    print("- Open approved Windows applications.")
    print("- Open approved websites.")
    print("- Open approved folders in File Explorer.")
    print("- Search the web using Google.")
    print("- Respond to basic text commands.")
    print("- Exit safely when requested.")

    print("More features will be added step by step!")


# ==========================================
# DATE AND TIME
# ==========================================

def show_time():
    """Display the computer's current local time."""

    current_time = datetime.now()

    print(
        f"{ASSISTANT_NAME}: Current time: "
        f"{current_time:%I:%M:%S %p}"
    )


def show_date():
    """Display the computer's current local date."""

    current_date = datetime.now()

    print(
        f"{ASSISTANT_NAME}: Today's date: "
        f"{current_date:%d %B %Y}"
    )


# ==========================================
# TIMER
# ==========================================

def start_timer(seconds):
    """Wait for the requested number of seconds."""

    print(
        f"{ASSISTANT_NAME}: Timer started for "
        f"{seconds} seconds."
    )

    try:
        time.sleep(seconds)
        print(f"{ASSISTANT_NAME}: Timer complete!")

    except KeyboardInterrupt:
        print(
            f"\n{ASSISTANT_NAME}: "
            "Timer interrupted by user."
        )


def handle_timer(command):
    """Validate the timer command and start it."""

    parts = command.split()

    if len(parts) != 2:
        print(f"{ASSISTANT_NAME}: Usage: timer <seconds>")
        return

    try:
        seconds = int(parts[1])

    except ValueError:
        print(
            f"{ASSISTANT_NAME}: "
            "Please enter a whole number of seconds."
        )
        return

    if seconds <= 0:
        print(
            f"{ASSISTANT_NAME}: "
            "Timer duration must be greater than zero."
        )
        return

    if seconds > 86400:
        print(
            f"{ASSISTANT_NAME}: "
            "Maximum timer duration is 86400 seconds (24 hours)."
        )
        return

    start_timer(seconds)


# ==========================================
# SYSTEM INFORMATION
# ==========================================

def show_system_info():
    """Display basic operating system and hardware information."""

    print(f"\n{ASSISTANT_NAME}: System Information")
    print("-" * 40)

    print(f"Operating System : {platform.system()}")
    print(f"OS Release       : {platform.release()}")
    print(f"OS Version       : {platform.version()}")
    print(f"Architecture     : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Logical CPU Cores: {os.cpu_count()}")
    print(f"Python Version   : {platform.python_version()}")

    print("-" * 40)


# ==========================================
# APPLICATION LAUNCHER
# ==========================================

def find_first_existing(paths):
    """Return the first existing executable file from approved paths."""

    for path in paths:
        if path and os.path.isfile(path):
            return os.path.abspath(path)

    return None


def resolve_application(app_name):
    """Resolve an approved application to an executable path."""

    system_root = os.environ.get("SystemRoot", r"C:\Windows")

    system_apps = {
        "notepad": os.path.join(
            system_root, "System32", "notepad.exe"
        ),
        "calculator": os.path.join(
            system_root, "System32", "calc.exe"
        ),
        "paint": os.path.join(
            system_root, "System32", "mspaint.exe"
        ),
    }

    if app_name in system_apps:
        path = system_apps[app_name]
        return path if os.path.isfile(path) else None

    if app_name == "vscode":
        candidates = [
            os.path.join(
                os.environ.get("LocalAppData", ""),
                "Programs", "Microsoft VS Code", "Code.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Microsoft VS Code", "Code.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Microsoft VS Code", "Code.exe"
            ),
        ]

        path = find_first_existing(candidates)

        # PATH fallback: useful for custom VS Code installations.
        # The resolved executable should be from a trusted installation.
        if path is None:
            path = shutil.which("code")

        return path

    if app_name == "chrome":
        candidates = [
            os.path.join(
                os.environ.get("ProgramFiles", ""),
                "Google", "Chrome", "Application", "chrome.exe"
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", ""),
                "Google", "Chrome", "Application", "chrome.exe"
            ),
            os.path.join(
                os.environ.get("LocalAppData", ""),
                "Google", "Chrome", "Application", "chrome.exe"
            ),
        ]

        return find_first_existing(candidates)

    return None


def open_application(app_name):
    """Launch an approved Windows application."""

    app_name = app_name.strip().casefold()

    if app_name not in APP_ALLOWLIST:
        print(
            f"{ASSISTANT_NAME}: Application "
            f"'{app_name}' is not in my approved list."
        )
        print(
            "Approved applications: "
            + ", ".join(APP_ALLOWLIST.keys())
        )
        return

    try:
        executable = resolve_application(app_name)

        if not executable:
            print(
                f"{ASSISTANT_NAME}: Could not find "
                f"{app_name}. Check its installation."
            )
            return

        subprocess.Popen(
            [executable],
            shell=False,
            close_fds=True
        )

        print(f"{ASSISTANT_NAME}: Opening {app_name}...")

    except OSError:
        print(
            f"{ASSISTANT_NAME}: "
            f"Could not open {app_name}."
        )


def handle_open_command(command):
    """Validate and handle application launch commands."""

    parts = command.split(maxsplit=1)

    if len(parts) != 2 or not parts[1].strip():
        print(
            f"{ASSISTANT_NAME}: "
            "Usage: open <application_name>"
        )
        return

    app_name = parts[1].strip()
    open_application(app_name)


# ==========================================
# WEBSITE LAUNCHER
# ==========================================

def open_website(website_name):
    """Open an approved website in the default browser."""

    website_name = website_name.strip().casefold()

    if website_name not in WEBSITE_ALLOWLIST:
        print(
            f"{ASSISTANT_NAME}: Website "
            f"'{website_name}' is not in my approved list."
        )
        print(
            "Approved websites: "
            + ", ".join(WEBSITE_ALLOWLIST.keys())
        )
        return

    try:
        url = WEBSITE_ALLOWLIST[website_name]
        opened = webbrowser.open(url)

        if opened:
            print(
                f"{ASSISTANT_NAME}: Opening "
                f"{website_name}..."
            )
        else:
            print(
                f"{ASSISTANT_NAME}: "
                "Could not open the website."
            )

    except Exception:
        print(
            f"{ASSISTANT_NAME}: "
            "An error occurred while opening the website."
        )


def handle_website_command(command):
    """Validate and handle website commands."""

    parts = command.split(maxsplit=1)

    if len(parts) != 2 or not parts[1].strip():
        print(
            f"{ASSISTANT_NAME}: "
            "Usage: website <website_name>"
        )
        return

    website_name = parts[1].strip()
    open_website(website_name)


# ==========================================
# FOLDER LAUNCHER
# ==========================================

def validate_folder_path(folder_path):
    """Validate that an approved folder exists and is a directory."""

    try:
        absolute_path = os.path.abspath(folder_path)
        resolved_path = os.path.realpath(absolute_path)

        if not os.path.isdir(resolved_path):
            return None

        return resolved_path

    except (OSError, ValueError):
        return None


def open_folder(folder_name):
    """Open an approved folder in Windows File Explorer."""

    folder_name = folder_name.strip().casefold()

    if folder_name not in FOLDER_ALLOWLIST:
        print(
            f"{ASSISTANT_NAME}: Folder "
            f"'{folder_name}' is not in my approved list."
        )
        print(
            "Approved folders: "
            + ", ".join(FOLDER_ALLOWLIST.keys())
        )
        return

    if platform.system() != "Windows":
        print(
            f"{ASSISTANT_NAME}: "
            "Folder opening is currently supported on Windows."
        )
        return

    folder_path = validate_folder_path(
        FOLDER_ALLOWLIST[folder_name]
    )

    if folder_path is None:
        print(
            f"{ASSISTANT_NAME}: "
            f"The folder '{folder_name}' does not exist "
            "or could not be validated."
        )
        return

    try:
        os.startfile(folder_path)
        print(f"{ASSISTANT_NAME}: Opening {folder_name}...")

    except OSError:
        print(
            f"{ASSISTANT_NAME}: "
            f"Could not open {folder_name}."
        )


def handle_folder_command(command):
    """Validate and handle folder commands."""

    parts = command.split(maxsplit=1)

    if len(parts) != 2 or not parts[1].strip():
        print(
            f"{ASSISTANT_NAME}: "
            "Usage: folder <folder_name>"
        )
        return

    folder_name = parts[1].strip()
    open_folder(folder_name)


# ==========================================
# WEB SEARCH
# ==========================================

def search_web(query):
    """Search Google using a URL-encoded query."""

    if not query.strip():
        print(
            f"{ASSISTANT_NAME}: "
            "Please enter something to search."
        )
        return

    encoded_query = quote_plus(query)

    search_url = (
        "https://www.google.com/search?q="
        + encoded_query
    )

    try:
        opened = webbrowser.open(search_url)

        if opened:
            print(
                f"{ASSISTANT_NAME}: "
                f"Searching Google for: {query}"
            )
        else:
            print(
                f"{ASSISTANT_NAME}: "
                "Could not open Google search."
            )

    except Exception:
        print(
            f"{ASSISTANT_NAME}: "
            "An error occurred during web search."
        )


def handle_search_command(command):
    """Extract the original search query and start web search."""

    parts = command.split(maxsplit=1)

    if len(parts) != 2 or not parts[1].strip():
        print(
            f"{ASSISTANT_NAME}: "
            "Usage: search <your search query>"
        )
        return

    query = parts[1].strip()
    search_web(query)


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():
    """Start the EVA command-line application."""

    show_greeting()

    while True:
        try:
            raw_command = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):
            print(
                f"\n{ASSISTANT_NAME}: "
                "Session interrupted. Goodbye!"
            )
            break

        # Preserve original input for search queries.
        normalized_command = raw_command.casefold()

        if normalized_command == "exit":
            print(
                f"{ASSISTANT_NAME}: "
                "Goodbye! See you again."
            )
            break

        elif normalized_command == "help":
            show_help()

        elif normalized_command in (
            "what can you do?",
            "what can you do"
        ):
            show_capabilities()

        elif normalized_command == "time":
            show_time()

        elif normalized_command == "date":
            show_date()

        elif normalized_command == "system":
            show_system_info()

        elif normalized_command == "timer" or normalized_command.startswith("timer "):
            handle_timer(raw_command)

        elif normalized_command == "open" or normalized_command.startswith("open "):
            handle_open_command(raw_command)

        elif normalized_command == "website" or normalized_command.startswith("website "):
            handle_website_command(raw_command)

        elif normalized_command == "folder" or normalized_command.startswith("folder "):
            handle_folder_command(raw_command)

        elif normalized_command == "search" or normalized_command.startswith("search "):
            handle_search_command(raw_command)

        elif normalized_command == "":
            continue

        else:
            print(
                f"{ASSISTANT_NAME}: "
                "I don't understand that command yet. "
                "Type 'help' to see available commands."
            )


if __name__ == "__main__":
    main()
