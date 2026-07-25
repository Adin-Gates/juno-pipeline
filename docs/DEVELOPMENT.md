## Development setup

Requires Python 3.13.


### First time on a machine
    python3 -m venv .venv

    source .venv/bin/activate        # Mac/Linux
    source .venv/Scripts/activate    # Windows Git Bash

    pip install -r requirements.txt


### Every session
    git pull

    source .venv/bin/activate        # Mac/Linux
    source .venv/Scripts/activate    # Windows Git Bash

    pip install -r requirements.txt  # only if requirements.txt changed


### After installing a new package
    pip freeze > requirements.txt
    git add requirements.txt && git commit -m "..."