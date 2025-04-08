import argparse
import os
import shutil


def save_backup(number, name=None):
    source = "/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita/save00"
    backup_name = (
        f"save00_backup_{number}_{name}" if name else f"save00_backup_{number}"
    )
    destination = os.path.join(os.path.dirname(source), backup_name)

    # Check if the destination exists and remove it if it does
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print("Removed existing backup.")

    shutil.copytree(source, destination)
    print(f"Backup created: {destination}")


def load_backup(number):
    source = f"/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita/save00_backup_{number}"
    destination = "/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita/save00"
    if os.path.exists(source):
        shutil.rmtree(destination)
        shutil.copytree(source, destination)
        print(f"Backup {number} loaded.")
    else:
        print(f"Backup {number} does not exist.")


def list_backups():
    directory = "/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita"
    backups = [d for d in os.listdir(directory) if d.startswith("save00_backup_")]
    print("Available backups:")
    for backup in backups:
        print(backup)


def main():
    parser = argparse.ArgumentParser(description="Manage Noita save backups.")
    subparsers = parser.add_subparsers(dest="command")

    save_parser = subparsers.add_parser("save", help="Save a backup")
    save_parser.add_argument("number", type=int, help="Backup number")
    save_parser.add_argument("--name", type=str, help="Optional name for the backup")

    load_parser = subparsers.add_parser("load", help="Load a backup")
    load_parser.add_argument("number", type=int, help="Backup number to load")

    subparsers.add_parser("list", help="List all backups")

    args = parser.parse_args()

    if args.command == "save":
        save_backup(args.number, args.name)
    elif args.command == "load":
        load_backup(args.number)
    elif args.command == "list":
        list_backups()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
