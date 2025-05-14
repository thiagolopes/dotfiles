from shutil import which
from dotbot import Plugin
import subprocess


class Flatpak(Plugin):
    _directive = "flatpak"

    def configure_flathub(self):
        command = "flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo"
        ret = subprocess.run(command.split(" "), capture_output=True)
        self._log.info("Flathub configured")

    def can_handle(self, directive):
        return self._directive == directive

    def handle(self, directive, data):
        if self._directive != directive:
            raise ValueError("flatpak cannot handle")

        if not which("flatpak"):
            self._log.error("Flatpak binary not available, skip operation...")
            return False

        if "flathub" in data and data["flathub"] is True:
            self.configure_flathub()

        if "packages" not in data:
            self._log.warning("Flatpak: 'packages' not found, skip install...")
            return True

        packages = data["packages"]
        if isinstance(packages, str):
            packages = packages.split(" ")

        command = "flatpak install {} -y".format(" ".join(packages))
        self._log.debug(command)

        return_process = subprocess.run(command.split(" "), capture_output=True)
        if return_process.returncode == 1:
            err = return_process.stderr.decode().split("\n")
            err = "Flatpak:\n" + "\n".join([e for e in err if e.startswith("error:")])
            self._log.error(err)
            return False

        ret = return_process.stderr.decode().rstrip().strip()
        self._log.lowinfo(ret)
        self._log.info("Flatpak finished")
        return True
