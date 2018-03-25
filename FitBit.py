#!/usr/bin/env python
import mysql.connector as mysql
import sys
import string
import re
import yaml
import optget

class FitBit(object):
	"""
	Creates an object that can parse the CSV file output from fitbit.com
	and insert the data into a MySQL/MariaDB database, per the provided
	schema
	"""
	def __init__(self):
		self._sections = {
			"Activities":self._add_activities,
			"Body":self._add_body,
			"Sleep":self._add_sleep,
			"Food Log":self._add_foodlog,
			"Daily Totals":self._add_nutrition,
		}
		self._connection = None
		self._cursor = None
		self._log = {}

	def load_file(self, fname):
		"""
		Loads the file and populates a data structure with entries
		"""

		meals = {'"Breakfast"':1, '"Lunch"':2, '"Dinner"':3, '"Morning Snack"':4, '"Afternoon Snack"':5, '"After Dinner"':7, '"Anytime"':8}	
		logdate = ""
		mealid = 0
		raw = open(fname,'r').read()
		raw = raw.split('\n\n')
		for section in raw:
			# parse the Body section of the CSV and store
			if re.search('Body',section) is not None:
				self._log["Body"] = []
				for line in section.split("\n")[2:]:
					self._log["Body"].append(self._parse_line(line))
			# parse the activities section of the CSV and store
			elif re.search('Activities',section) is not None:
				self._log["Activities"] = []
				for line in section.split("\n")[2:]:
					self._log["Activities"].append(self._parse_line(line))
			# parse the food log entry
			elif re.search('Food Log', section) is not None:
				nut = [] # store the nutrition info temporarily
				if not "Food Log" in self._log:
					self._log["Food Log"] = {}
				if not "Daily Totals" in self._log:
					self._log["Daily Totals"] = {}
				food, nutrition = section.split("Daily Totals")
				# main food log 		
				for line in food.split("\n"):
					if "Log" in line:
						date = line[-8:]
						logdate = date[0:4] + "-" + date[4:6] + "-" + date[6:]
						self._log["Food Log"][logdate] = []
						self._log["Daily Totals"][logdate] = []
					elif line in meals:
						mealid = meals[line]
					else:
						self._parse_foodlog(logdate,mealid,line)
				# daily nutrition stats
				for line in nutrition.split("\n"):
					val = line.split('","')[-1:][0][:-1]
					if len(val) > 0:
						nut.append(val)
				self._log["Daily Totals"][logdate] = nut
			# sleep stats
			elif re.search("Sleep", section) is not None:
				self._log["Sleep"] = []
				for line in section.split("\n")[2:]:
					self._log["Sleep"].append(self._parse_line(line))
			# we don't really need this. info is present in nutrition stats
			elif re.search("Foods",section) is not None:
				pass
	def connectdb(self,u,p,h,d):
		"""
		Takes the necessary arguments to mysql.connect and creates a connection
		context and cursor internally to the FitBit object
		"""
		self._connection = mysql.connect(user=u,password=p,host=h,database=d)
		self._cursor = self._connection.cursor()
	
	def insert_data(self):
		"""
		Inserts all the data from the datastructure into the database
		"""
		assert self._connection is not None, "No connection exists"
		assert self._cursor is not None, "No cursor exists"
		for key in self._log.keys():
			self._sections[key](self._log[key])	
	
	def dbcommit(self):
		"""
		Commit the database transaction
		"""
		self._connection.commit()
	
	def dbclose(self):
		"""
		Close the database connection and cursor
		"""
		self._cursor.close()
		self._connection.close()		
	
	def _add_activities(self, entries):
		"""
		Build the query for activities and actually insert into fbact
		"""
		for ent in entries:
			query = """INSERT INTO fbact
				(days, calsburned, steps, distance, floors, ms, mla, mfa, mva, actcals)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			self._cursor.execute(query,ent)
	
	def _add_body(self, entries):
		"""
		Build the query for body and actually insert into body
		"""
		for ent in entries:
			query = """INSERT INTO body (days, weight, bmi, fat) VALUES (%s, %s, %s, %s)"""
			self._cursor.execute(query,ent)
	
	def _add_foodlog(self, data):
		""" 
		build the query for the food log and insert
		"""
		for date in data:
			for ent in data[date]:
				ent.insert(0,date)
				query = """INSERT INTO foodlog (days, meal, food, calories) VALUES (%s, %s, %s, %s)"""
				self._cursor.execute(query,ent) 	
	def _add_nutrition(self, data):
		"""
		build the query for the nutrition stats and insert
		"""
		for date in data:
			data[date].insert(0,date)	
			query = """INSERT INTO nutrition (days, calories, fat, fiber, carbs, sodium, protein, water) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
			#self._cursor.execute(query,data[date])	
	
	def _add_sleep(self, entries):
		"""
		build the query for the sleep stats and insert
		"""
		for ent in entries:
			query = """INSERT INTO sleep
				(starttime, endtime, minsleep, minwake, numwakes, minbed, minrem, minlight, mindeep)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			#self._cursor.execute(query,ent)			
	
	def _parse_line(self, entry):
		"""
		Cleans up a line and returns a list of values
		"""
		fields = entry.split('","')
		fields[0] = fields[0][1:]
		fields[-1] = fields[-1][:-1]
		clean = []
		for field in fields:
			if ',' in field:
				field = field.translate(None,string.punctuation)
			elif field == "N/A":
				field = None
			if field == "":
				continue	
			clean.append(field)
		return clean 

	def _parse_foodlog(self,date,mealid,entry):
		"""
		parse food log entries and store in the data structure
		"""
		if "Meal" in entry:
			pass
		else:
			data = self._parse_line(entry)
			if len(data) == 0:
				return
			else:
				data.insert(0,mealid)
				self._log["Food Log"][date].append(data)
# end FitBit
