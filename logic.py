import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Coding', 'People skills', 'Cooking', 'Languages'])] # skills that may be needed for different sort of jobs
professions = [ (_,) for _ in (["Nurse", "Developer", "Teacher", "Cook", "Translator"])]
jobs_profession = [ (_,) for _ in ([1,2,3,4,5])]
jobs_skills_id = [ (_,) for _ in ([[2,4], [1,4], [2,4], [3], [2,4] ])]
class Manager:
    def __init__(self, database):
        self.database = database

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()

        # main table for jobs and skills they require
        cur.execute("CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY, profession INTEGER, skills_id INTEGER, FOREIGN KEY(profession) REFERENCES professions(id), FOREIGN KEY(skills_id) REFERENCES skills(id))")

        # main table for the name of the professions
        cur.execute("CREATE TABLE IF NOT EXISTS professions(id INTEGER PRIMARY KEY, name TEXT)")

        # main table for skills/interests
        cur.execute("CREATE TABLE IF NOT EXISTS skills(id INTEGER PRIMARY KEY, skill_name TEXT)")

        # main table for saving skills of the user
        cur.execute("CREATE TABLE IF NOT EXISTS user_info(id INTEGER PRIMARY KEY, user_id INTEGER, skills_id INTEGER, FOREIGN KEY(skills_id) REFERENCES skills(id))")

        conn.commit() # commit the creation of the databases
        conn.close() #close the connection

    def default_insert(self):
        sql = 'INSERT OR IGNORE INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT OR IGNORE INTO professions (name) values(?)'
        data = professions
        self.__executemany(sql, data)
        # Comes in the way of manual insertion
#        sql = 'INSERT OR IGNORE INTO jobs (profession) values(?)'
#        data = jobs_profession
#        self.__executemany(sql, data)


    # function to add a skill into users data
    def insert_project(self, data):
        sql = """INSERT OR IGNORE INTO user_info (skill_id) values(?)""" # Запиши сюда правильный SQL запрос
        self.__executemany(sql, data)

    # Selects all skills tied to a user_id
    def select_user_skills(self,userid):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        cur.execute(f"SELECT skills_id WHERE user_id = {userid}")

    # Simply fetches all users
    def get_users(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id FROM user_info")     
            return [x[0] for x in cur.fetchall()]

    # function to add users into the database
    def insert_user(self,data):
        sql = """INSERT OR IGNORE INTO user_info (user_id) values(?)"""
        self.__executemany(sql,data)

    # function to delete a skill from the users data
    def delete_skill(self, project_id, skill_id):
        sql = """DELETE FROM skills WHERE skill_id = ? AND skill_id = ? """ # Запиши сюда правильный SQL запрос
        self.__executemany(sql, [(skill_id, project_id)])


if __name__ == '__main__':
    manager = Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
    # Not sure how to implement auto-insertion of skills for corresponding professions into the jobs table
    # Therefore I inserted them manually