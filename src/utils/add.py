from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from rich import print as printc

import utils.aesutil
from utils.dbConfig import dbconfig


def computeMasterKey(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key

def addEntry(mp, ds, sitename, siteurl, email, username, ):
    # get the password
    password = getpass("Password: ")

    mk = computeMasterKey(mp, ds)
    encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")

    # Add to database
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO pm.entries (sitename, siteurl, email, username, password) VALUES (%s, %s, %s, %s, %s)"
    values = (sitename, siteurl, email, username, encrypted)
    cursor.execute(query, values)
    db.commit()

    printc("[green][+][/green] Entry added")
    db.close()