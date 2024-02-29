# Secret Keeper
CLI Python Password Manager

## Configuration

To configure your database, make sure you have MySQL installed and running. Then, run the following command:

python3 config.py

## Usage

### Adding a New Item

To add a new item to the password manager, use the following command. The only required field is the site name. Optionally, you can provide the site URL, email, and username.

python3 pm.py add -n {sitename} -u {siteurl} -e {email} -l {username}

### Extracting Items

To extract all items from the password manager, use the following command:

python3 pm.py extract

To extract a single item and copy it to your clipboard, provide the site name with the --copy flag:

python3 pm.py extract -n {sitename} --copy

### Generating a Password

To generate a password, specify the desired length. The generated password will be automatically copied to your clipboard.

python3 pm.py generate --length {length}

## Notes

- Replace {sitename}, {siteurl}, {email}, {username}, and {length} with appropriate values.
- Ensure you have the necessary permissions and dependencies installed before running the commands.
- Make sure to keep your database configuration secure and backed up regularly.
