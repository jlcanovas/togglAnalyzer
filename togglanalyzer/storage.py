import mysql.connector


class TogglStorage(object):

    def __init__(self, config):
        self.config = config

    def init_db(self, force=False):
        """Inits the database, creating the required tables"""

        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)

        query = "SHOW TABLES LIKE 'entry'"
        cursor = cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            print 'Entry tables already exists.'

        if result is not None and not force:
            print 'Launch the script with the -f option'
            return

        if result is not None and force:
            print 'Deleting entry table'
            drop_table_entry = 'DROP TABLE IF EXISTS entry;'
            cursor = cnx.cursor()
            cursor.execute(drop_table_entry)
            cursor.close()

        print 'Creating entry table'
        create_table_entry = "CREATE TABLE entry( " \
                             "id int(20) PRIMARY KEY, " \
                             "description varchar(255), " \
                             "start timestamp, " \
                             "end timestamp, " \
                             "user varchar(255), " \
                             "project varchar(255), " \
                             "INDEX useri (user), " \
                             "INDEX projecti (project) " \
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"
        cursor = cnx.cursor()
        cursor.execute(create_table_entry)
        cursor.close()

    def add_entry(self, id, description, start, end, user, project):
        """Adds a new entry to the entry table"""
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)

        cursor = cnx.cursor()
        query = "INSERT IGNORE INTO entry(id, description, start, end, user, project) VALUES (%s, %s, %s, %s, %s, %s)"
        digested_start = start.replace('T', ' ')
        digested_start = digested_start[:-6]
        digested_end = end.replace('T', ' ')
        digested_end = digested_end[:-6]
        arguments = [id, description, digested_start, digested_end, user, project]
        cursor.execute(query, arguments)
        cnx.commit()
        cursor.close()
