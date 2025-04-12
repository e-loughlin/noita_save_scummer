import argparse
import os
import shutil
import time
from datetime import datetime


SAVE_DIR = "/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita"
SAVE00 = os.path.join(SAVE_DIR, "save00")


def save_backup(number=None, name=None, timestamp=False):
    if timestamp:
        name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"save00_backup_{name}"
    else:
        backup_name = f"save00_backup_{number}_{name}" if name else f"save00_backup_{number}"

    destination = os.path.join(SAVE_DIR, backup_name)

    if os.path.exists(destination):
        shutil.rmtree(destination)
        print("Removed existing backup.")

    shutil.copytree(SAVE00, destination)
    print(f"Backup created: {destination}")


def load_backup(identifier):
    if identifier == "recent":
        backup = get_most_recent_backup()
        if backup is None:
            print("No backups available.")
            return
        source = os.path.join(SAVE_DIR, backup)
        print(f"Loading most recent backup: {backup}")
    else:
        source = os.path.join(SAVE_DIR, f"save00_backup_{identifier}")

    if not os.path.exists(source):
        print(f"Backup {identifier} does not exist.")
        return

    if os.path.exists(SAVE00):
        shutil.rmtree(SAVE00)
    shutil.copytree(source, SAVE00)
    print(f"Backup {identifier} loaded.")


def list_backups():
    backups = [d for d in os.listdir(SAVE_DIR) if d.startswith("save00_backup_")]
    backups.sort(reverse=True)
    print("Available backups:")
    for backup in backups:
        print(backup)


def get_most_recent_backup():
    backups = [
        d for d in os.listdir(SAVE_DIR)
        if d.startswith("save00_backup_") and os.path.isdir(os.path.join(SAVE_DIR, d))
    ]
    if not backups:
        return None
    backups.sort(key=lambda d: os.path.getmtime(os.path.join(SAVE_DIR, d)), reverse=True)
    return backups[0]


def prune_old_backups(max_backups=10):
    backups = [
        d for d in os.listdir(SAVE_DIR)
        if d.startswith("save00_backup_") and os.path.isdir(os.path.join(SAVE_DIR, d))
    ]
    backups.sort(key=lambda d: os.path.getmtime(os.path.join(SAVE_DIR, d)), reverse=True)
    for old_backup in backups[max_backups:]:
        path = os.path.join(SAVE_DIR, old_backup)
        shutil.rmtree(path)
        print(f"Deleted old backup: {old_backup}")


def autosave_loop(interval_minutes=2):
    print("Autosaving every 2 minutes... Press Ctrl+C to stop.")
    try:
        while True:
            save_backup(timestamp=True)
            prune_old_backups()
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\nAutosave stopped by user.")


def main():
    parser = argparse.ArgumentParser(description="Manage Noita save backups.")
    subparsers = parser.add_subparsers(dest="command")

    save_parser = subparsers.add_parser("save", help="Save a backup")
    save_parser.add_argument("number", type=int, help="Backup number")
    save_parser.add_argument("--name", type=str, help="Optional name for the backup")

    load_parser = subparsers.add_parser("load", help="Load a backup")
    load_parser.add_argument("identifier", type=str, help="Backup number or 'recent'")

    subparsers.add_parser("list", help="List all backups")
    subparsers.add_parser("autosave", help="Run autosave every 2 minutes")

    args = parser.parse_args()

    if args.command == "save":
        save_backup(args.number, args.name)
    elif args.command == "load":
        load_backup(args.identifier)
    elif args.command == "list":
        list_backups()
    elif args.command == "autosave":
        autosave_loop()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

