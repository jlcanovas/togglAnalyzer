import config
import sys, getopt
from togglanalyzer import storage
from togglanalyzer import analyzer
import requests
import re
from datetime import datetime

""" Usage of this script """
USAGE = "run.py -i | -r <repo_name> | -q <repo_name> \n" \
        "Main options:\n" \
        "  -i      - inits the database (-f option is required if the table already exists)\n" \
        "  -s date - starting date (format YYYY-MM-DD)\n" \
        "  -e date - ending date (format YYYY-MM-DD)\n"


def connection_alive():
    """Checks if internet connection is working. We use Google"""
    try:
        requests.get('http://www.google.com', timeout=10)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except:
        return False


def main(argv):
    if len(argv) == 0:
        print USAGE
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hifs:e:", [])
    except getopt.GetoptError:
        print USAGE
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print USAGE
            sys.exit()
        elif opt in '-i':
            force_option = False
            user_based = False
            for opt2, arg2 in opts:
                if opt2 in '-f':
                    force_option = True
            toggl_storage = storage.TogglStorage(config)
            toggl_storage.init_db(force_option)
            sys.exit(0)
        elif opt in '-s':
            starting_date = arg
            for opt3, arg3 in opts:
                if opt3 in '-e':
                    ending_date = arg3

            # Checking format for dates
            checker = re.compile('.{4}-.{2}-.{2}')
            if len(starting_date) < 10 or len(ending_date) < 10 or not checker.match(starting_date) or not checker.match(ending_date):
                print 'The dates should follow the format YYYY-MM-DD'
                sys.exit(2)

            datetime_starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
            datetime_ending_date = datetime.strptime(ending_date, '%Y-%m-%d')
            if datetime_ending_date < datetime_starting_date:
                print 'Ending date can not be before Starting date'
                sys.exit(2)

            print 'Testing connection'
            if not connection_alive():
                print "No internet connection was detected"
                sys.exit()
            print "Internet connection was detected. Good!"

            toggl_analyzer = analyzer.TogglAnalyzer(config)
            toggl_analyzer.retrieve(starting_date, ending_date)

if __name__ == '__main__':
    main(sys.argv[1:])
