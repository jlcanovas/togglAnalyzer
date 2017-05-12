I use this repository as a playground to test Toggl API. 

## Current support

The tool currently retrieves the set of entry details in Toggl for a given workspace and export them to a mysql database.

## Installation

To install this project, follow these steps:

* This project has been developed in Python 2.7, so first you have to [install Python](https://www.python.org/) in your machine.
* Clone this repository
* Navigate to the path where you cloned this repo and execute:

```
pip install
```

* Copy (or rename) ```config.py-example``` to ```config.py```. This file sets the main variables to configure the tool.

## Executing the tool

The repo includes the script ```run.py``` which helps you to execute the tool. 
First of all, you have to configure the main variables used in the process and defined in ```config.py``` file. 
The variables are:

* ```API_TOKEN```, the token given by Toggl to use their API (you can find it in your [user account details](https://www.toggl.com/app/profile)
* ```WORKSPACE```, the workspace identifier to be analyzed
* ```DATABASE```, the name of the schema database where the info will be stored
* ```USER```, the database user
* ```PASSWORD```, the database password
* ```HOST```, the database host
* ```PORT```, the database port

Once configured, you can execute the tool by calling first: 

```
python run.py -i
```

which will initialize the database creating the required tables. Then call: 

```
python run.py -s 2017-05-01 -e 2017-05-10
```

The tool will connect to your workspace using your API token, retrieve all the entries for the timespan specified 
(starting at the date set in the argument ```-s``` an ending at the date set in the argument ```-e```)
and store them in the database.



 

