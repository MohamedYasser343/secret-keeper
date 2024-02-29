import sys
from utils.dbConfig import dbconfig
from getpass import getpass
import hashlib
import string
import random

from rich import print as printc
from rich.console import Console

def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def config():
    # Create a Database
    db = dbconfig()
    cursor = db.cursor()
    printc("[green][+] Creating new config [/green]")
    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc("[red][!] An error occured while trying to create the database.")
        Console.print_exception(show_locals=True)
        sys.exit(0)
    printc("[green][+][/green] Database 'pm' created")

    # Create Tables
    query = "CREATE TABLE pm.secrets (masterKey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL UNIQUE, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    while 1:
        mp = getpass("Choose a master password: ")
        if mp==getpass("Re-type: ") and mp!="":
            break
        printc("[yellow][-] Please try again.[/yellow]")
    
    # Hash the master password
    hashed_mp = hashlib.sha256(mp.encode('utf-8')).hexdigest()
    printc("[green][+][/green] Hashing master password")

    # Generate device secret
    ds = generateDeviceSecret()

    # Add them to database
    query = "INSERT INTO pm.secrets (masterKey_hash, device_secret) VALUES (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Master password and device secret added to database")
    printc("[green][+][/green] Configured successfully!")
    db.close()


config()