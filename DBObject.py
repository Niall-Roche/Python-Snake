import sqlite3

TABLE_NAMES = [
                'PLAYERS',
                'SETTINGS'
              ]

tbl_players = """CREATE TABLE PLAYERS(
                       ID        INT   PRIMARY KEY  NOT NULL,
                       NAME      TEXT               NOT NULL,
                       SCORE     INT                NOT NULL
              )"""

tbl_settings = """CREATE TABLE SETTINGS(
                       MAX_LEN          INT,
                       APPLE_NO         INT
              )"""


INSERTS = """
            DELETE FROM SETTINGS;
            INSERT INTO SETTINGS(MAX_LEN, APPLE_NO) VALUES('5','3');
          """

class DBO(object):
    """docstring for DBO."""
    def __init__(self, conn_string):
        self.__conn_string = conn_string
        self.connection = sqlite3.connect(self.__conn_string)
        self.connection.row_factory = sqlite3.Row
        self.__tables()

    def __tables(self):
        c = self.connection.cursor()

        for name in TABLE_NAMES:
            if c.execute("select name from sqlite_master where type = 'table' and upper(name) = ?", (name,)).fetchone() is None:
                c.execute(self.__tables_dict(name))
        c.executescript(INSERTS)
        self.connection.commit()


    def __tables_dict(self, name):
        return {
            'PLAYERS': tbl_players,
            'SETTINGS': tbl_settings
        }[name]
