from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parents[2]


if __name__ == "__main__":
    print(get_project_root())
