import sqlite3, random, datetime
from models import Food

def getNewId():
	return random.getrandbits(28)

foods = [
	{
	'name': 'Peanut butter',
	'quantity': '1 jar',
	'timestamp': datetime.datetime.now()
	},
	{
	'name': 'Bread',
	'quantity': '2 loaves',
	'timestamp': datetime.datetime.now()
	},
	{
	'name': 'Pasta',
	'quantity': '2 boxes',
	'timestamp': datetime.datetime.now()
	},
	{
	'name': 'Pasta sauce Raos',
	'quantity': '1 jar',
	'timestamp': datetime.datetime.now()
	}

]

def connect():
    conn = sqlite3.connect('foods.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, name TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in foods:
        fd = Food(getNewId(), i['name'], i['timestamp'])
        insert(fd)

def insert(food):
	conn = sqlite3.connect('foods.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO foods VALUES (?,?,?,?)", (
		food.id,
		food.name,
		food.timestamp
	))
	conn.commit()
	conn.close()

def view():
    conn = sqlite3.connect('foods.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM foods")
    rows = cur.fetchall()
    foods = []
    for i in rows:
        food = Food(i[0], True if i[1] == 1 else False, i[2], i[3])
        foods.append(food)
    conn.close()
    return foods

def update(food):
    conn = sqlite3.connect('foods.db')
    cur = conn.cursor()
    cur.execute("UPDATE foods SET name=? WHERE id=?", (food.name, food.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('foods.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM foods WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('foods.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM foods")
    conn.commit()
    conn.close()
