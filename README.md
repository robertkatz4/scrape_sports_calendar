# Internet scrape/upload of schedules into a Google Calendar
I scrape the NBA schedule and insert the events into an existing Google Calendar.

To deploy:
- Create a conda environment `pip install -r requirments.txt`

```
conda install google-api-python-client
pip install --upgrade google-api-python-client oauth2client
```

To authenticate with the Google API, download credentials from the Google Developer console, and rename the file `client_secret.json` in the working directory.

`python run.py --noauth_local_webserver`

will open the browser and reveal a code to copy/paste into the terminal. This process puts a json file in the `~/.credentials` folder locally that will allow the `python run.py` to use the google API.

A few notes on the packages - I had to use the following as the most recent versions of each did not work. These have been added to the requirements.txt file.
xml==3.6.4
twisted=16.6.0
