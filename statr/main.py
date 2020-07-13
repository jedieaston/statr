# Get status for Canvas every 5 minutes and report back....

import requests as r
import json
# import sys
import click



def get_status(url) -> tuple:
    # Gets the current status for the first item on this page, which in our case is Canvas.
    url += "/api/v2/components.json"
    content = r.get(url)
    content = json.loads(content.content)
    return content["components"][0]["name"], content["components"][0]["status"]

def wrapper(url) -> str:
    """
    Gets status from a statuspage. and returns if its up or not.
    """

    name, result = get_status(url)
    if (result == "operational"):
        return (name + " is up.")
    elif (result == "major_outage"):
        return (name + " is down. Current status ==", result)
    else:
        return (name + " may be down. Current status ==", result)

@click.command()
@click.option('--url', default="https://status.instructure.com/", help="URL of Statuspage.io statuspage.")
def cli(url):
    """
    returns status from a statuspage.io page to STDOUT.
    """
    try:
        click.echo(wrapper(url))
    except:
        click.echo("Bad URL! Try again.")


if __name__ == "__main__":
    cli()
    

