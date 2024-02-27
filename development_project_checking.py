import argparse
import subprocess

from pathlib import Path

ENV_SUBFOLDERS = ["Include", "Lib", "Scripts"]


def python_project_validation(folder_path: Path) -> Path | list[Path] | None:
    env_path = folder_path / "env"

    if env_path.is_dir() and all(
        (env_path / subfolder).is_dir() for subfolder in ENV_SUBFOLDERS
    ):
        return env_path

    python_files = [f for f in folder_path.iterdir() if f.suffix == ".py"]
    if python_files:
        return python_files

    return None


def freeze_command(env_path) -> list[Path | str]:
    return [env_path / "Scripts" / "python", "-m", "pip", "freeze"]


def ask_for_requirements_file(project_path: Path, env_path: Path) -> None:
    user_decision = input("  ? Do you want to generate one? (y/n): ")

    if user_decision.lower() == "y":
        generate_requirements_file(project_path, env_path)


def generate_requirements_file(project_path: Path, env_path: Path) -> None:
    requirements_file = project_path / "requirements.txt"

    subprocess.run(
        freeze_command(env_path),
        cwd=project_path,
        text=True,
        stdout=open(requirements_file, "w"),
    )

    print("  > Generated requirements.txt file")


def check_requirements_file(project_path: Path, env_path: Path) -> None:
    requirements_file = project_path / "requirements.txt"

    if not requirements_file.exists():
        print("  ! No requirements.txt found.")
        ask_for_requirements_file(project_path, env_path)
        return

    with requirements_file.open("r", encoding="utf-8") as f:
        file_requirements = [l.rstrip() for l in f.readlines()]

    current_requirements = subprocess.check_output(
        freeze_command(env_path),
        cwd=project_path,
        text=True,
    ).splitlines()

    if sorted(file_requirements) != sorted(current_requirements):
        print("  ! Difference between requirements.txt and pip freeze")
        print(file_requirements)
        print(current_requirements)
        # ask_for_requirements_file(project_path, env_path)


def has_git_repository(project_path: Path) -> bool:
    try:
        git_status_output = subprocess.check_output(
            ["git", "-C", project_path, "status"],
            stderr=subprocess.STDOUT,
            text=True,
        )

        if "nothing to commit, working tree clean" not in git_status_output:
            print("  ! Git pending changes detected")

        return True
    except subprocess.CalledProcessError:
        print("  x No Git repo detected")
        return False


def has_git_ignore(project_path: Path) -> bool:
    return (project_path / ".gitignore").exists()


def iterate_dir(root: Path) -> None:
    for parent, dirs, _ in root.walk():
        subdirs = dirs[:]

        for dir in subdirs:
            project_path = parent / dir
            project_validation = python_project_validation(project_path)

            if project_validation:
                print("-" * 10)
                print(project_path)

                if has_git_repository(project_path):
                    if not has_git_ignore(project_path):
                        print("  ! .gitignore not detected")

                if isinstance(project_validation, Path):
                    check_requirements_file(project_path, project_validation)
                else:
                    print("  ! No 'Env' folder detected")

                dirs.remove(dir)

                print()


def main() -> None:
    iterate_dir(Path(r"D:\Users\joel_\Development\python"))


if __name__ == "__main__":
    main()
