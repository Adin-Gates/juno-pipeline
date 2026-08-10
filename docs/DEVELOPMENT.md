## Development setup

Requires Python 3.13.


### First time on a machine
    python3 -m venv .venv

    source .venv/bin/activate        # Mac/Linux
    source .venv/Scripts/activate    # Windows Git Bash

    pip install -e ".[dev]"


### Every session
    git pull

    source .venv/bin/activate        # Mac/Linux
    source .venv/Scripts/activate    # Windows Git Bash

    pip install -e ".[dev]"          # only if packages have been added to dependencies


### After installing a new package
   add package to pyproject.toml under "dependencies" if it is run dependend
   add package to pyproject.toml under "project.optional-dependencies" if it is dev only


### Linux Workstation Setup
    nvidia driver version 580DKMS - if we update kernel this could break
    /show UUID - aac52f71-3791-407d-b659-4d528b3fb356

    Autodesk maya needed an Identity Manager update to 1.15 or higher.
    Needed to be X11 instead of Wayland
    Make sure to run in terminal to check if any libraries are missing
