from pathlib import Path


# Get the folder where your project is located
PROJECT_FOLDER = Path(__file__).resolve().parent


def save_content(content, filename="ai_content.txt"):

    # Save directly inside the project folder
    file_path = PROJECT_FOLDER / filename

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def read_content(filename="ai_content.txt"):

    file_path = PROJECT_FOLDER / filename

    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()