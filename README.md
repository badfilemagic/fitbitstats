# fitbitstats
scripts for parsing the csv exported from fitbit.com, storing data in a mysql/mariadb database, and doing stuff with it

1. Create the database and configure it so it can be connected to
2. Edit the config.yml file with the relevant information
3. run fbprocess.py like:
	./fbprocess -c config.yml
	Note: command line arguments will override what is in the config file.

