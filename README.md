# Noita Save Scummer

This script helps manage backups of your Noita game saves using command-line arguments. It allows you to save, load, and list backups of your game progress.

## Requirements

- Python 3.x
- `argparse` module (included in the Python standard library)

## Usage

The script provides three main functionalities: `save`, `load`, and `list`.

### Save a Backup

To save a backup of your current game progress:

```bash
python noita_save_scummer.py save <Number> [--name <name>]
```

- `<Number>`: A required integer to identify the backup.
- `--name <name>`: An optional name to further identify the backup.

Example:

```bash
python noita_save_scummer.py save 1 --name "before_boss"
```

### Load a Backup

To load a previously saved backup:

```bash
python noita_save_scummer.py load <Number>
```

- `<Number>`: The integer identifier of the backup you want to load.

Example:

```bash
python noita_save_scummer.py load 1
```

### List All Backups

To list all available backups:

```bash
python noita_save_scummer.py list
```

This will display all backups in the directory.

## Directory Structure

The script operates on the following directory:

```
/home/deck/.steam/steam/steamapps/compatdata/881100/pfx/drive_c/users/steamuser/AppData/LocalLow/Nolla_Games_Noita/
```

Backups are stored in the format `save00_backup_<Number>_<name>`.

## License

This project is licensed under the MIT License.
