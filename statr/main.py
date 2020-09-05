import requests as r
import json
# import sys
import click
import os
import subprocess
from pathlib import Path
from click_default_group import DefaultGroup


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
    # First... do we have internet?
    response = subprocess.run(["ping", "-c", "1", "-i", "0.2", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode 
    if (response != 0):
        print("It doesn't appear you have internet. So everything's down!")
        raise click.Abort()
    name, result = get_status(url)
    if (result == "operational"):
        return (name + " is up.")
    elif (result == "major_outage"):
        return (name + " is down. Current status ==", result)
    elif (result == "degraded_performance"):
        return (f"{name} is degraded.")
    elif (result == "partial_outage."):
        return(f"{name} is partially down.")
    else:
        return (name + " may be down. Current status ==", result)

def get_bookmarks() -> dict:
    """ 
    Returns all of the bookmarks in a dict. If it can't open the file or its empty, it returns an empty dict.
    """
    try:
        with open(os.path.join(Path.home(), ".config/statr.json")) as f:
            try:
                return json.loads(f.read())
            except:
                # It's empty!
                return {}
    except:
        # The file doesn't exist!
        return {}

@click.command()
@click.argument('url')
def url_check(url):
    """
    returns status from a statuspage.io page to STDOUT.
    """
    try:
        click.echo(wrapper(url))
    except:
        click.echo("Bad URL! Try again.")

@click.command()   
@click.argument('save', type=(str, str))
def save_bookmark(save):
    """
    Saves a service so you don't have to type the URL. Arguments: save <name> <url>
    """
    # First, make sure they gave us a valid thing.
    name, url = save
    try:
        wrapper(url)
    except:
        click.echo("Bad URL! Did you type the arguments incorrectly?")
        raise click.Abort()
    # It's valid. Now let's make sure it's not already saved.
    
    bookmarks = get_bookmarks()
    check = bookmarks.get(name, "nope")
    if (check != "nope"):
        click.echo("This name already exists! Choose a different one or remove it from ~/.config/statr.json")
        # exit()
        raise click.Abort()
    # Now let's write it!
    try:
        bookmarks[name] = url
        # Does .config exist?
        if (os.path.exists(os.path.join(Path.home(), ".config/")) == False):
            # Let's create it!
            os.mkdir(os.path.join(Path.home(), ".config/"))
        # We have .config now!
        with open(os.path.join(Path.home(), ".config/statr.json"), "w+") as f:
            f.write(json.dumps(bookmarks))
    except:
        click.echo("We couldn't save the bookmark. Ensure that you have write access to ~/.config/statr.json and try again.")
        raise click.Abort()
    click.echo(name + " saved to statr.json. to check, run 'statr service " + name + "'")

@click.command()
@click.argument('service')
def check_service(service):
    """
    Check a particular service that you saved via save. Arguments: service <name>
    """
    bookmarks = get_bookmarks()
    try:
        url = bookmarks[service]
    except:
        print("That service is not defined in ~/.config/statr.json. Try to save it first!")
        raise click.Abort()
    try:
        click.echo(wrapper(url))
    except:
        click.echo("The URL that is saved isn't valid. Check ~/.config/statr.json and try again")
        raise click.Abort()

@click.command()
def check_all():
    """
    Checks all services that have been saved.
    """
    bookmarks = get_bookmarks()
    if (bookmarks == {}):
        print("You haven't defined any services yet! Run 'statr --help' for more info.")
    else:
        for i in list(bookmarks.values()):
            try:
                click.echo(wrapper(str(i)))
            except click.Abort:
                click.Abort()
            except:
                click.echo("We can't check " + str(i) + " . Check that it's correct in ~/.config/statr.json")
                exit()

@click.group(cls=DefaultGroup, default="check-all", default_if_no_args=True)
def cli():
    """
    Check the status of a service via its statuspage.io page!
    """

# add the commands.
cli.add_command(url_check, name='url')
cli.add_command(save_bookmark, name='save')
cli.add_command(check_service, name='service')
cli.add_command(check_all)
cli.set_default_command(check_all)

if __name__ == "__main__":
    cli()
    

