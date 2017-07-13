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
            print 'There are tables in the database!'

        if result is not None and not force:
            print 'Launch the script with the -f option'
            return

        if result is not None and force:
            print 'Deleting tables'
            drop_table_entry = 'DROP TABLE IF EXISTS entry;'
            drop_table_project = 'DROP TABLE IF EXISTS project;'
            drop_table_tag = 'DROP TABLE IF EXISTS tag;'
            drop_table_entry_tag = 'DROP TABLE IF EXISTS entry_tag;'
            cursor = cnx.cursor()
            cursor.execute(drop_table_entry)
            cursor.execute(drop_table_project)
            cursor.execute(drop_table_tag)
            cursor.execute(drop_table_entry_tag)
            cursor.close()

        print 'Creating entry table'
        create_table_entry = "CREATE TABLE entry( " \
                             "id int(20) PRIMARY KEY, " \
                             "description varchar(255), " \
                             "start timestamp, " \
                             "end timestamp, " \
                             "user varchar(255), " \
                             "project int(20), " \
                             "INDEX useri (user), " \
                             "INDEX projecti (project) " \
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"
        cursor = cnx.cursor()
        cursor.execute(create_table_entry)

        print 'Creating project table'
        create_table_project = "CREATE TABLE project( " \
                             "id int(20) AUTO_INCREMENT PRIMARY KEY, " \
                             "name varchar(255), " \
                             "INDEX namei (name) " \
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"
        cursor = cnx.cursor()
        cursor.execute(create_table_project)

        print 'Creating tag table'
        create_table_tag = "CREATE TABLE tag( " \
                             "id int(20) AUTO_INCREMENT PRIMARY KEY, " \
                             "name varchar(255), " \
                             "INDEX namei (name) " \
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"
        cursor = cnx.cursor()
        cursor.execute(create_table_tag)
        cursor.close()

        print 'Creating entry_tag table'
        create_table_entry_tag = "CREATE TABLE entry_tag( " \
                             "entry_id int(20), " \
                             "tag_id int(20), " \
                             "PRIMARY KEY tagentryi (entry_id, tag_id) " \
                             ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"
        cursor = cnx.cursor()
        cursor.execute(create_table_entry_tag)
        cursor.close()

    def add_project(self, project):
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)
        cursor = cnx.cursor()
        query = "INSERT IGNORE INTO project(name) VALUES (%s)"
        arguments = [project]
        cursor.execute(query, arguments)
        cnx.commit()
        cursor.close()

    def add_tag(self, tag):
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)
        cursor = cnx.cursor()
        query = "INSERT IGNORE INTO tag(name) VALUES (%s)"
        arguments = [tag]
        cursor.execute(query, arguments)
        cnx.commit()
        cursor.close()

    def add_entry_tag(self, entry, tag):
        tag_id = self.get_tag_id(tag)
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)
        cursor = cnx.cursor()
        query = "INSERT IGNORE INTO entry_tag(entry_id, tag_id) VALUES (%s, %s)"
        arguments = [entry, tag_id]
        cursor.execute(query, arguments)
        cnx.commit()
        cursor.close()

    def get_tag_id(self, tag):
        """
        Utility function to obtain the id of a tag
        :param tag: Name of the tag
        """
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)
        cursor = cnx.cursor()
        query = "SELECT id FROM tag WHERE name = %s"
        arguments = [tag]
        cursor.execute(query, arguments)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            self.add_tag(tag)
            return self.get_tag_id(tag)
        repo_id = result[0]
        cnx.close()
        return repo_id

    def get_project_id(self, project):
        """
        Utility function to obtain the id of a project
        :param project: Name of the project
        """
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)
        cursor = cnx.cursor()
        query = "SELECT id FROM project WHERE name = %s"
        arguments = [project]
        cursor.execute(query, arguments)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            self.add_project(project)
            return self.get_project_id(project)
        repo_id = result[0]
        cnx.close()
        return repo_id

    def add_entry(self, id, description, start, end, user, project, tags):
        """Adds a new entry to the entry table"""
        cnx = mysql.connector.connect(user=self.config.USER, password=self.config.PASSWORD, database=self.config.DATABASE, host=self.config.HOST, port=self.config.PORT, raise_on_warnings=True, buffered=True)

        cursor = cnx.cursor()
        query = "INSERT IGNORE INTO entry(id, description, start, end, user, project) VALUES (%s, %s, %s, %s, %s, %s)"
        digested_start = start.replace('T', ' ')
        digested_start = digested_start[:-6]
        digested_end = end.replace('T', ' ')
        digested_end = digested_end[:-6]
        project_id = self.get_project_id(project)
        arguments = [id, description, digested_start, digested_end, user, project_id]
        cursor.execute(query, arguments)
        cnx.commit()
        cursor.close()
        for tag in tags:
            self.add_entry_tag(id, tag)
