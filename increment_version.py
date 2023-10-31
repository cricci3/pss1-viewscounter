import re
import argparse

def increment_version(version, increment_type):
    major, minor, patch = map(int, version.split('.'))

    if increment_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif increment_type == 'minor':
        minor += 1
        patch = 0
    elif increment_type == 'patch':
        patch += 1

    return f"{major}.{minor}.{patch}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('increment_type', choices=['major', 'minor', 'patch'], help='Increment type (major, minor, or patch)')
    args = parser.parse_args()

    with open('setup.py', 'r', encoding='utf-8') as file:
        setup_content = file.read()

    version_pattern = r"version\s*=\s*['\"](\d+\.\d+\.\d+)['\"]"
    match = re.search(version_pattern, setup_content)

    if match:
        current_version = match.group(1)
        new_version = increment_version(current_version, args.increment_type)
        updated_setup = re.sub(version_pattern, f"version='{new_version}'", setup_content)

        with open('setup.py', 'w', encoding='utf-8') as file:
            file.write(updated_setup)


if __name__ == "__main__":
    main()
