"""Small module to load a yaml config."""

from pathlib import Path

import yaml


def load_config(config_path: Path | str) -> dict:
    """Load a YAML configuration file as dictionary.

    - If given a directory, it ensures there is exactly one YAML file and loads it.
    - If given a file path (with or without .yaml extension), it loads the specified file.
    - If the file or directory is invalid, it raises an appropriate error.

    Args:
        config_path (Path | str): Path to the configuration file or directory.

    Returns:
        dict: Parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If a directory is given but contains no or multiple YAML files.
        yaml.YAMLError: If the YAML file cannot be parsed.
    """
    if isinstance(config_path, str):
        config_path = Path(config_path)

    # Handle case where a directory is given
    if config_path.is_dir():
        yaml_files = list(config_path.glob("*.yaml"))
        if len(yaml_files) == 0:
            raise ValueError(
                f"Error: No YAML configuration file found in directory '{config_path}'."
            )
        if len(yaml_files) > 1:
            raise ValueError(
                f"Error: Multiple YAML files found in directory '{config_path}'. "
                "Expected exactly one."
            )
        config_path = Path(yaml_files[0])

    # If no extension is given, assume ".yaml"
    if config_path.suffix == "":
        config_path = config_path.with_suffix(".yaml")

    # If its not a yaml file, stop
    if config_path.suffix != ".yaml":
        raise ValueError(
            "Invalid file extension. Expected a .yaml file but the extension was: "
            f"{config_path.suffix}"
        )

    # Check if the file exists
    if not config_path.exists():
        raise FileNotFoundError(f"Error: Configuration file '{config_path}' not found.")

    # Load and parse the YAML file
    try:
        with open(config_path, encoding="utf-8") as file:
            config = yaml.safe_load(
                file
            )  # Safe loading to avoid arbitrary code execution
        return config
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(f"Error loading YAML file '{config_path}': {exc}")
