from shutil import which
from dotbot import Plugin
import subprocess


class Flatpak(Plugin):
    _directive = "flatpak"
    _command = "flatpak install -y --user {package}"
    _command_repo = "flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo"

    def can_handle(self, directive):
        return self._directive == directive

    def handle(self, directive, data):
        if self._directive != directive:
            raise ValueError("flatpak cannot handle")
        return self._process(data)

    def process_install(self, package):
        command = self._command.format(package=package)
        return_process = subprocess.run(command.split(" "), capture_output=True)

        err = return_process.stderr.decode()

        if return_process.returncode == 1:
            err = err.split("\n")
            err_out = "Flatpak:" + "\n".join([e for e in err if e.startswith("error:")])
            self._log.error(err_out)
            return False

        ret = err.rstrip().strip().replace("\n", " ")
        if not ret:
            self._log.info(f"Installed: {package}")
        else:
            self._log.lowinfo(ret)
        return True

    def _process(self, data):
        if not which("flatpak"):
            self._log.error("Flatpak binary not found, skip this step...")
            return False

        if "flathub" in data and data["flathub"] is True:
            self.configure_flathub()

        if "packages" not in data:
            self._log.warning("Flatpak: 'packages' not found, skip install...")
            return True

        packages = data["packages"]
        if isinstance(packages, str):
            packages = packages.split(" ")

        for package in packages:
            self.process_install(package)

        self._log.info("Flatpak finished")
        return True

    def configure_flathub(self):
        ret = subprocess.run(self._command_repo.split(" "), capture_output=True)
        self._log.info("Flathub repo configured")
