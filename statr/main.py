# Get status for Canvas every 5 minutes and report back....
#!/usr/bin/env python

import requests as r
import json
import sys


def get_status(url) -> tuple:
    # Gets the current status for the first item on this page, which in our case is Canvas.
    url += "/api/v2/components.json"
    content = r.get(url)
    content = json.loads(content.content)
    return content["components"][0]["name"], content["components"][0]["status"]

def wrapper(url) -> str:
    name, result = get_status(url)
    if (result == "operational"):
        return (name + " is up.")
    elif (result == "major_outage"):
        return (name + " is down. Current status ==", result)
    else:
        return (name + " may be down. Current status ==", result)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        # we were passed a different url.
        try:
            print(wrapper(sys.argv[1]))
        except:
            print("That statuspage(tm) is not available!")
    else:
        # Guess we'll just do Canvas.
        print (wrapper("https://status.instructure.com/"))
        exit()

    

