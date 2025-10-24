#!/usr/bin/env python3
"""
OS Detection and Package Manager Utility
Detects Linux distribution and provides appropriate package manager commands
"""

import platform
import subprocess
import os


class OSDetector:
    def __init__(self):
        self.system = platform.system()
        self.distro = None
        self.package_manager = None
        self._detect_distro()

    def _detect_distro(self):
        """Detect Linux distribution and package manager"""
        if self.system != "Linux":
            return

        # Try to read /etc/os-release
        try:
            with open('/etc/os-release', 'r') as f:
                os_release = f.read()

            if 'ubuntu' in os_release.lower() or 'debian' in os_release.lower():
                self.distro = 'debian'
                self.package_manager = 'apt'
            elif 'fedora' in os_release.lower():
                self.distro = 'fedora'
                self.package_manager = 'dnf'
            elif 'centos' in os_release.lower() or 'rhel' in os_release.lower():
                self.distro = 'rhel'
                self.package_manager = 'yum'
            elif 'arch' in os_release.lower():
                self.distro = 'arch'
                self.package_manager = 'pacman'
            elif 'opensuse' in os_release.lower():
                self.distro = 'opensuse'
                self.package_manager = 'zypper'
            else:
                self.distro = 'unknown'
                self.package_manager = 'unknown'
        except Exception as e:
            print(f"Error detecting distro: {e}")
            self.distro = 'unknown'
            self.package_manager = 'unknown'

    def get_install_command(self, packages):
        """Get package installation command for current distro"""
        if isinstance(packages, str):
            packages = [packages]

        pkg_string = ' '.join(packages)

        commands = {
            'apt': f'sudo apt update && sudo apt install -y {pkg_string}',
            'dnf': f'sudo dnf install -y {pkg_string}',
            'yum': f'sudo yum install -y {pkg_string}',
            'pacman': f'sudo pacman -S --noconfirm {pkg_string}',
            'zypper': f'sudo zypper install -y {pkg_string}'
        }

        return commands.get(self.package_manager, f'# Unknown package manager, install: {pkg_string}')

    def check_command_exists(self, command):
        """Check if a command exists on the system"""
        try:
            subprocess.run(['which', command],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def get_python_tk_package(self):
        """Get the appropriate python-tk package name for the distro"""
        packages = {
            'apt': ['python3-tk'],
            'dnf': ['python3-tkinter'],
            'yum': ['python3-tkinter'],
            'pacman': ['tk'],
            'zypper': ['python3-tk']
        }
        return packages.get(self.package_manager, ['python3-tk'])

    def get_info(self):
        """Get system information"""
        return {
            'system': self.system,
            'distro': self.distro,
            'package_manager': self.package_manager,
            'python_version': platform.python_version()
        }


if __name__ == '__main__':
    detector = OSDetector()
    info = detector.get_info()
    print("System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    print(f"\nSample install command: {detector.get_install_command(['curl', 'git'])}")
