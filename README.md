# ePaper Calendar

Playing around with my new waveshare 7in3g e-paper screen, going to try and render a calendar

# WARNING

There's something a bit screwy around "burn in" I've read both that it occurs and also that it doesn't occur.  Try to avoid leaving the screen with stuff on it for more than a day, if you want it always on, do the clear thing at least daily so it jiggles all those pixels around.

TODO: add venv instructions
# venv
Keep the python peas from touching the other python carrots

create a venv using:
```
python -m venv .venv
```

## windows
put powershell into venv mode using:
```
.\venv\Scripts\activate.ps1
```

## linux
put powershell into venv mode using:
```
source ./venv/Scripts/activate
```

# Dependencies


## system
The thing requires a few system dependencies.  
This is really only relevant on the pi itself, which is running a debian thingy, so apt-get with:
```
TODO: add system dependencies
```

## pip
python dependencies are managed in `requirements.txt`
when in venv mode install using:
```
pip install -r requirements.txt
```
TODO: add waveshare dependencies to requirements.txt

# Runtime

TODO: add runtime instructions
## Google Authentication

TODO: change to one where I can scan a QR code and do it on my phone

## Rendering

TODO: calendar name to avatar
TODO: small chip on left with avatar & time, summary on right with larger text
TODO: center day headings

