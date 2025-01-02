# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2022-2025 Graz University of Technology.
#
# Invenio-Cli is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module to ease the creation and management of applications."""

import sys
from os import listdir

from ..helpers.process import ProcessResponse
from .steps import CommandStep


class PackagesCommands:
    """Local installation commands."""

    def __init__(self, cli_config):
        """Construct PackagesCommands."""
        self.cli_config = cli_config

    def install_packages(self, packages, log_file=None):
        """Steps to install Python packages.

        It is a class method since it does not require any configuration.
        """
        match self.cli_config.python_packages_manager:
            case "uv":
                cmd = ["uv", "pip", "install"]
            case "pip":
                cmd = ["pipenv", "run", "pip", "install"]
            case _:
                print("please configure python package manager.")
                sys.exit()

        for package in packages:
            cmd.extend(["-e", package])

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message="Installing python dependencies...",
                log_file=log_file,
            )
        ]

        return steps

    def outdated_packages(self):
        """Steps to show outdated packages.

        It is a class method since it does not require any configuration.
        """

        match self.cli_config.python_packages_manager:
            case "uv":
                raise RuntimeError("not yet ported to uv")
            case "pip":
                cmd = ["pipenv", "update", "--outdated"]
            case _:
                print("please configure python package manager.")
                sys.exit()

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message="Checking outdated packages...",
            )
        ]

        return steps

    def update_packages(self):
        """Steps to update all Python packages.

        It is a class method since it does not require any configuration.
        """
        match self.cli_config.python_packages_manager:
            case "uv":
                cmd = ["uv", "sync", "--upgrade"]
            case "pip":
                cmd = ["pipenv", "update"]
            case _:
                print("please configure python package manager.")
                sys.exit()

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message="Updating package(s)...",
            )
        ]

        return steps

    def update_package_new_version(self, package, version):
        """Update invenio-app-rdm version.

        It is a class method since it does not require any configuration.
        """
        match self.cli_config.python_packages_manager:
            case "uv":
                raise RuntimeError("not yet ported to uv")
            case "pip":
                cmd = ["pipenv", "install", package + version]
            case _:
                print("please configure python package manager.")
                sys.exit()

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message=f"Updating {package} to version {version}...",
            )
        ]

        return steps

    def install_locked_dependencies(self, pre, dev):
        """Install dependencies from requirements.txt using install."""
        match self.cli_config.python_packages_manager:
            case "uv":
                cmd = ["uv", "sync"]
            case "pip":
                cmd = ["pipenv", "sync"]
                if pre:
                    cmd += ["--pre"]
                if dev:
                    cmd += ["--dev"]
            case _:
                print("please configure python package manager.")
                sys.exit()

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message="Installing python dependencies... Please be "
                + "patient, this operation might take some time...",
            )
        ]

        return steps

    def lock(self, pre, dev):
        """Steps to lock Python dependencies."""
        match self.cli_config.python_packages_manager:
            case "uv":
                cmd = ["uv", "lock"]
            case "pip":
                cmd = ["pipenv", "lock"]
                if pre:
                    cmd += ["--pre"]
                if dev:
                    cmd += ["--dev"]
            case _:
                print("please configure python package manager.")
                sys.exit()

        steps = [
            CommandStep(
                cmd=cmd,
                env={"PIPENV_VERBOSITY": "-1"},
                message="Locking python dependencies...",
            )
        ]

        return steps

    def is_locked(self):
        """Checks if the dependencies have been locked."""

        match self.cli_config.python_packages_manager:
            case "uv":
                locked = "uv.lock" in listdir(".")
            case "pip":
                locked = "Pipfile.lock" in listdir(".")
            case _:
                print("please configure python package manager.")
                sys.exit()

        if not locked:
            return ProcessResponse(
                error="Dependencies were not locked. "
                + "Please run `invenio-cli packages lock`.",
                status_code=1,
            )

        return ProcessResponse(
            output="Dependencies are locked",
            status_code=0,
        )
