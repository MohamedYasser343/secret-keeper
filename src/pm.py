import argparse
from getpass import getpass
import hashlib
import pyperclip

from rich import print as printc

import utils.add
import utils.retrieve
import utils.generate
from utils.dbConfig import dbconfig

def inputAndValidateMasterPassword():
    mp = getpass("MASTER PASSWORD: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchone()
    if not result or hashed_mp != result[0]:
        printc("[red][!] WRONG MASTER PASSWORD! [/red]")
        return None

    return [mp, result[1]]

def main():
    parser = argparse.ArgumentParser(description='Password Manager')

    parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
    parser.add_argument("-n", "--sitename", help="Site name")
    parser.add_argument("-u", "--siteurl", help="Site URL")
    parser.add_argument("-e", "--email", help="Email")
    parser.add_argument("-l", "--username", help="Username")
    parser.add_argument("--length", help="Length of the password to generate", type=int)
    parser.add_argument("-c", "--copy", action='store_true', help='Copy password to clipboard')

    args = parser.parse_args()

    if args.option in ["add", "a"]:
        required_fields = ['sitename', 'siteurl', 'username']
        missing_fields = [field for field in required_fields if getattr(args, field) is None]
        if missing_fields:
            printc("[red][!] Missing required fields: {} [/red]".format(', '.join(missing_fields)))
            return

        args.email = args.email or ""

        res = inputAndValidateMasterPassword()
        if res:
            utils.add.addEntry(res[0], res[1], args.sitename, args.siteurl, args.email, args.username)

    elif args.option in ["extract", "e"]:
        res = inputAndValidateMasterPassword()

        search = {key: getattr(args, key) for key in ['sitename', 'siteurl', 'email', 'username'] if getattr(args, key) is not None}
        if res:
            utils.retrieve.retrieveEntries(res[0], res[1], search, decryptPassword=args.copy)

    elif args.option in ["generate", "g"]:
        password = utils.generate.generatePassword(args.length)
        pyperclip.copy(password)
        printc("[green][+] Password generated and copied to clipboard [/green]")

if __name__ == "__main__":
    main()
