import mysql.connector as mysql
import sys, string
import re


FILENAME = "data.csv"


def add_activity(args):
	query = """INSERT INTO fbact
		(days, calsburned, steps, distance, floors, ms, mla, mfa, mva, actcals)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	
	cursor.execute(query, args)

def add_body(args):
	query = """INSERT INTO body (days, weight, bmi, fat) VALUES (%s, %s, %s, %s)"""
	cursor.execute(query, args)

def add_sleep(args):
	query = """INSERT INTO sleep
		(starttime, endtime, minsleep, minwake, numwakes, minbed, minrem, minlight, mindeep)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	cursor.execute(query,args)

def parse_line(entry):
	fields = entry.split('","')
	fields[0] = fields[0][1:]
	fields[-1] = fields[-1][:-1]
	clean = []
	for field in fields:
		if ',' in field:
			field = field.translate(None,string.punctuation)
		elif field == "N/A":
			field = None
		clean.append(field)
				
	return clean


def parse_foodlog(log):
	assert type(log) is list, "parse_foodlog expects a list as an argument"
	meals = {'"Breakfast"':1, '"Lunch"':2, '"Dinner"':3, '"Morning Snack"':4, '"Afternoon Snack"':5, '"After Dinner"':7, '"Anytime"':8}
	logdate = ""
	mealid = 0
	ins = ""
	nutrition_stats = []
	daily_nut = []
	for ent in log:
		if ent == "":
			if len(daily_nut) > 0:
				nutrition_stats.append(daily_nut)
			continue
		if "Log" in ent:
			date = ent[-8:]
			logdate = date[0:4] + "-" + date[4:6] + "-" + date[6:]
			ins = "Food Log"
		elif "Daily Totals" in ent:
			daily_nut = [logdate]
			ins = "Daily Totals"
			continue
		elif ent in meals:
			mealid = meals[ent]
			continue	
		elif ent == "Meal,Food,Calories":
			continue
		else:
			entries = []
			fields = parse_line(ent)
			entries.append(logdate)
			if ins == "Food Log":
				entries.append(mealid)
				for x in fields:
					if len(x) > 0:
						entries.append(x)
				add_foodlog(entries)
			elif ins == "Daily Totals":
				daily_nut.append(fields[-1])
	for nutrition in nutrition_stats:
		add_nutrition(nutrition)	

def add_foods(args):
	pass

def add_foodlog(args):
	query = """INSERT INTO foodlog (days, meal, food, calories) VALUES (%s, %s, %s, %s)"""
	cursor.execute(query, args)

def add_nutrition(args):
	query = """INSERT INTO nutrition (days, calories, fat, fiber, carbs, sodium, protein, water) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
	#cursor.execute(query,args)

inserter = {
	"Activities":add_activity,
	"Body":add_body,
	"Sleep":add_sleep,
	"Food Log":add_foodlog,
	"Daily Toals":add_nutrition,
	"Foods":add_foods,
}	


if __name__ == '__main__':
	lines = [line.rstrip() for line in open(sys.argv[1], 'r').readlines()]
	foodlogdata = []	
	cnx = mysql.connect(user='stats', password='stats', host='192.168.72.132', database='healthstats')	
	cursor = cnx.cursor()	
	parser = "" 
	i = 0
	for line in lines:
		if line in inserter:
			parser = line
			i += 1
		elif "Date" in line:
			i += 1
			continue
		elif "Start Time" in line: 
			i += 1
			continue
		elif line == "":
			i += 1
			continue
		elif "Food Log" in line:
			foodlogdata = lines[i:]
			break	
		else:
			inserter[parser](parse_line(line))
			i += 1
	if len(foodlogdata) > 0:
		parse_foodlog(foodlogdata)
	cnx.commit()
	cursor.close()
	cnx.close()
