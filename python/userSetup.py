print("Juno: userSetup.py ran")

import datetime

with open("/tmp/juno-usersetup.log", "a") as f:
    f.write(f"userSetup ran at {datetime.datetime.now()}\n")
