import sqlite3

conn = sqlite3.connect('orgdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
fh = open(fname)
orgs = []
for line in fh:    
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    #change in logic
    parts = email.split('@')
    org = parts[-1]    
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( org, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (org, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()


rows = cur.execute('SELECT * FROM Counts ORDER BY count DESC')
for row in rows:
    print(row[0],row[1])

cur.close()

      


