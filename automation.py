import shutil
from pathlib import Path

import click
import httpx
import yaml
from loguru import logger


def load_config():
    try:
        with open("config.yaml") as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logger.error("The config.yaml file was not found.")
        raise
    except yaml.YAMLError:
        logger.error("Error parsing the YAML file.")
        raise


def create_folder(year: int, day_number: int):
    year_dir = f"{year}"
    year_path = Path(year_dir)
    try:
        year_path.mkdir(exist_ok=True)
    except PermissionError:
        logger.error(
            f"Permission error: Could not create folder fo{year_dir}."
        )
        raise

    day_dir = f"day{day_number}"
    day_path = year_path / day_dir

    try:
        day_path.mkdir(exist_ok=True)
    except PermissionError:
        logger.error(f"Permission error: Could not create {day_dir}.")
        raise

    for folder in ["src", "test", "data"]:
        folder_path = day_path / folder
        folder_path.mkdir(exist_ok=True)  # Ensure directory exists

    create_readme(day_number, day_path, year)
    add_templates(day_number, day_path)

    logger.info(f"Created structure for {year}, Day{day_number} challenge.")


def add_templates(day_number, day_path):
    template_solution_path = "0_template_files/solution_template.py"
    template_test_path = "0_template_files/test_solution_template.py"
    new_solution_name = f"solution_day{day_number}.py"
    new_test_name = f"test_day{day_number}.py"
    full_solution_path = day_path / "src" / new_solution_name
    full_test_path = day_path / "test" / new_test_name
    shutil.copy(template_solution_path, full_solution_path)
    shutil.copy(template_test_path, full_test_path)


def create_readme(day_number: int, day_path: Path, year: int):
    readme_content = (
        f"# Advent of Code - {year} -  Day {day_number}\n"
        f"\n Description and notes for Day{day_number} challenge"
    )
    readme_file = day_path / "NOTES.md"
    with open(readme_file, "w") as file:
        file.write(readme_content)


def fetch_data(url: str, headers: dict) -> httpx.Response:
    try:
        with httpx.AsyncClient() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response
    except httpx.HTTPError as e:
        logger.error(f"An HTTP error occurred: {e}")
        raise


async def save_input(day_number: int, year: int, session_cookie: str):
    url = f"https://adventofcode.com/{year}/day/{day_number}/input"
    headers = {"cookie": f"session={session_cookie}"}

    response = fetch_data(url, headers)
    if response.is_success:
        day_path = Path(f"{year}/day{day_number}")
        data_file = day_path / "data" / "challenge_input_data.txt"
        with data_file.open("wb") as file:
            file.write(response.content)
        logger.info(f"Downloaded challenge data for Day {day_number}.")
    else:
        logger.error(f"Failed to download input data for Day {day_number}.")


@click.command()
@click.argument("year", type=int)
@click.argument("day_number", type=int)
def get_puzzle(year, day_number):
    try:
        config = load_config()
        session_cookie = config["Credentials"]["session_cookie"]

        if create_folder(year, day_number):
            save_input(day_number, year, session_cookie)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    get_puzzle()
