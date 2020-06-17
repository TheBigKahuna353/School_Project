import sqlite3 as sql

db_file = 'database.db'

db = sql.connect(db_file)

cursor = db.cursor()

def get_questions(hunt):
    action = '''
    SELECT 
    Question_text
    FROM Hunt_questions JOIN Questions ON Question_id = Questions.id
    WHERE Hunt_questions.Hunt_id = %d;
    ''' % (hunt+1)
    
    cursor.execute(action)
    
    a = cursor.fetchall()
    print(a)
    return a[0]

def get_all_hunts():
    action = '''
    SELECT
    hunt_name
    FROM hunts
    '''
    
    cursor.execute(action)
    
    a = cursor.fetchall()
    print(a)
    return a

def num_hunts():
    return len(get_all_hunts())