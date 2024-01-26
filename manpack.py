import os
import subprocess
import platform
import distro
import pandas as pd


def get_packages(path: str):
    # The list of the dictionaries with a package name and its version
    packages = []

    # Open a csv file with data
    pkg_table = pd.read_csv(path)

    for index, row in pkg_table.iterrows():
        packages.append({ 
            "package" : row.package_name, 
            "command" : row.command,
            "version" : str(row.preferred_version)
        })

    return packages


def get_pkg_manager():
    pkg_manager = None
    # Determine the package manager
    os_name = platform.system().lower()

    if os_name == "linux":
        distro_name = distro.id().lower()

        if distro_name in ["ubuntu", "debian"]:
            pkg_manager = "apt-get"
        elif distro_name in ["fedora"]:
            pkg_manager = "dnf"
        elif distro_name in ["centos", "rhel", "redhat"]:
            pkg_manager = "yum"

    elif os_name == "darwin":
        # Check for Homebrew on macOS
        brew_path = subprocess.run(["which", "brew"], stdout=subprocess.PIPE, text=True).stdout.strip()

        if brew_path:
            # Homebrew is installed, use it
            pkg_manager = brew_path

    else:
        raise ValueError("Unsupported OS")

    if pkg_manager == None:
        raise ValueError("Unsupported the distributive!")

    return pkg_manager


def install_package(package_name, action, version=None):
    """
    Install or update a specific package to a given version.
    If no version is provided, the latest available version is installed.
    """
    # To get the correct package manager of the system
    pkg_manager = get_pkg_manager()

    # Construct the package install command
    if version:
        if pkg_manager.endswith("brew"):
            package = f"{package_name}@{version}"
        else:
            package = f"{package_name}-{version}"
    else:
        package = package_name

    command = [pkg_manager, action, package]
    if pkg_manager in ["apt-get", "yum"]:
        command.insert(1, 'sudo')  # Add 'sudo' for these package managers

    # Run the package install command
    try:
        subprocess.run(command, check=True)
        print(f"Package {package} installed/updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing/updating {package}: {e}")


# Entry point of the program
def main():
    # Example usage:
    #install_package('tree', "update")  # Replace with your package name and version
    packages = get_packages("packages.csv")

    for pkg in packages:
        print(pkg['package'], pkg['command'], pkg['version'])
        install_package(pkg['package'], pkg['command'], pkg['version'])


if __name__ == '__main__':
    main()






