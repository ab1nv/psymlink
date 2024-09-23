import os
import shutil
import sys


def create_symlink(source, destination, base_dir):
    """Create a symlink and handle existing destination. Works for both files and directories."""
    source = os.path.join(base_dir, source)
    destination = os.path.expanduser(destination)

    if not os.path.exists(source):
        print(f"Source {source} does not exist. Skipping.")
        return

    if os.path.exists(destination):
        print(f"Destination {destination} already exists.")
        while True:
            user_input = input(
                f"Do you want to overwrite (o), skip (s), or backup (b) {destination}?"
            ).lower()
            if user_input == "o":
                if os.path.isdir(destination) and not os.path.islink(destination):
                    shutil.rmtree(destination)
                else:
                    os.remove(destination)
                break
            elif user_input == "s":
                print(f"Skipping {destination}")
                return
            elif user_input == "b":
                backup_destination = destination + ".bak"
                shutil.move(destination, backup_destination)
                print(f"Backup created at {backup_destination}")
                break
            else:
                print("Invalid input. Please enter 'o', 's', or 'b'.")

    if os.path.isdir(source):
        create_directory_symlink(source, destination)
    else:
        create_file_symlink(source, destination)


def create_file_symlink(source, destination):
    try:
        print(f"Creating symlink from {source} to {destination}")
        os.symlink(source, destination)
    except OSError as e:
        print(f"Failed to create symlink: {e}")


def create_directory_symlink(source, destination):
    try:
        if (
            os.name == "nt"
        ):  # Windows requires `target_is_directory=True` for directory symlinks
            print(
                f"Creating directory symlink (Windows) from {source} to {destination}"
            )
            os.symlink(source, destination, target_is_directory=True)
        else:
            print(f"Creating symlink from {source} to {destination}")
            os.symlink(source, destination)
    except OSError as e:
        print(f"Failed to create symlink: {e}")


def process_symlinks(file_mappings, base_dir):
    """Process symlink creation for each entry in the file mappings."""
    for _, paths in file_mappings.items():
        for source, destination in paths.items():
            create_symlink(source, destination, base_dir)


def prompt_create_map_py():
    """Prompt user to create map.py with an example."""
    print("\nError: Could not find 'map.py' or illegal format found.")
    print(
        "Please create a 'map.py' file in the same directory with the following format:"
    )
    print(
        """
Example of 'map.py':

file_name = {
    "bashrc": {
        "bash/bashrc": "~/.bashrc" # File symlink
    },
    "config_directory": {
        ".config": "~/.config/my_config_dir"  # Directory symlink
    }
}
"""
    )


if __name__ == "__main__":
    try:
        import map  # type: ignore

        base_dir = os.path.dirname(os.path.abspath(__file__))

        if isinstance(map.file_name, dict):
            process_symlinks(map.file_name, base_dir)
        else:
            prompt_create_map_py()

    except ImportError:
        prompt_create_map_py()
        sys.exit(1)
