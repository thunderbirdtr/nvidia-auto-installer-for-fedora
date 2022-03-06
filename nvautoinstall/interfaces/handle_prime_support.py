"""
NVIDIA Auto Installer for Fedora Linux
Copyright (C) 2019-2021 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import sys

from click import style

from . import (
    Objc_CheckSuperuserPermissions,
    Objc_HandleDriversInstallation,
    Objc_HandlePrimeSupport,
    Objc_HandleRPMFusionRepositories,
    failure,
    general,
    section,
    success,
    warning,
)


class HandlePrimeSupport:
    def __init__(self):
        section("CHECKING SUPERUSER PERMISSIONS...")
        if Objc_CheckSuperuserPermissions.main():
            success("Superuser privilege acquired")
            section("CHECKING AVAILABILITY OF RPM FUSION NVIDIA REPOSITORY...")
            if Objc_HandleRPMFusionRepositories.avbl():
                warning("RPM Fusion repository for Proprietary NVIDIA Driver was detected")
                section("ATTEMPTING CONNECTION TO RPM FUSION SERVERS...")
                if Objc_HandleRPMFusionRepositories.conn():
                    success("Connection to RPM Fusion servers was established")
                    section("LOOKING FOR EXISTING DRIVER PACKAGES...")
                    data = Objc_HandleDriversInstallation.avbl()
                    if data is False:
                        failure("No existing NVIDIA driver packages were detected")
                    else:
                        qant = 0
                        for indx in data:
                            if indx != "":
                                qant += 1
                                general(indx)
                        warning("A total of " + str(qant) + " driver packages were detected")
                        section("SETTING UP PRIME SUPPORT...")
                        warning("Intervention required")
                        general(style("< Y >", fg="green", bold=True) + " to enable PRIME support")
                        general(style("< N >", fg="red", bold=True) + " to disable PRIME support")
                        general(style("< * >", fg="yellow", bold=True) + " anything else to leave")
                        solution = input("[Y/N] ")
                        if solution == "Y" or solution == "y":
                            section("ENABLING PRIME SUPPORT...")
                            if Objc_HandlePrimeSupport.main(True):
                                success("PRIME Support was successfully enabled")
                            else:
                                failure("PRIME Support could not be enabled")
                        elif solution == "N" or solution == "n":
                            section("DISABLING PRIME SUPPORT...")
                            if Objc_HandlePrimeSupport.main(False):
                                success("PRIME Support was successfully disabled")
                            else:
                                failure("PRIME Support could not be disabled")
                        else:
                            section("SAFE AND GOOD ANSWER...")
                else:
                    failure("Connection to RPM Fusion servers could not be established")
            else:
                failure("RPM Fusion repository for Proprietary NVIDIA Driver was not detected")
        else:
            failure("Superuser privilege could not be acquired")
        failure("Leaving installer")
        sys.exit(0)