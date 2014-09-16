
import glob
import re
import pickle 


filenames = glob.glob("./*.txt")

total_set = dict()

for filename in filenames:
	f = open(filename,"rb")

	print "filename: %s" % (filename,)

	current_team = None

	yearly_games = []

	for line in f.readlines():

		spread = None
		overunder = None
		other_team = ""
		wORl = None
		team_score = None
		otherteam_score = None
		date = None


		if re.search("^[A-Z]\.[0-9]", line):
			#print "game: %s" % (line,)
			game_array = line.split()
			#date = game_array[0]
			#other_team = game_array[1]
			#print "date: %s" % (date,)
			#print "other_team: %s" % (other_team,)
			for item in game_array:
				if re.search("^[uon]", item):
					#print "over_under: %s" % (item,)
					overunder = item
				elif re.search("^\+[0-9]", item) or re.search("^\-[0-9]", item):
					#print "spread: %s" % (item,)
					spread_list = item.split('\'')
					spread = float(spread_list[0])
					if len(spread_list) == 2:
						spread += 0.5
				elif re.search("^P$", item):
					spread = None
				elif re.search("^[WL]$", item):
					#print "W/L: %s" % (item,)
					wORl = item
				elif re.search("[0-9]+\-[0-9]", item):
					#print "Score: %s" % (item,)
					team_score = item.split('-')[0]
					otherteam_score = item.split('-')[1]
					if team_score != None:
						team_score = int(team_score)
					if otherteam_score != None:
						otherteam_score = int(otherteam_score)
				elif re.search("^[A-Z]\.[0-9]", item):
					#print "Date: %s" % (item,)
					date = item
				elif re.search("^\(.+\)$", item):
					#print "Special item: %s" % (item,)
					continue
				elif re.search("[A-Za-z]+", item) or re.search("&",item):
					#print "part of other_team?: %s" % (item,)
					other_team += item
				else:
					#print "weird item: %s" % (item,)
					continue




		elif re.search("^$", line):
			#print "empty line"
			continue

		elif re.search( "^\(" , line) or re.search( "^\^", line):
			#print "extra line: %s" % (line,)
			continue

		elif re.search( "[A-Z]+", line):
			#print "TEAM: %s" % (line,)
			current_team = line.strip()
			current_team = current_team.split('(')[0]
			current_team = current_team.strip()
			continue

		else:
			#print "unknown: %s" % (line)
			continue

		print "%s: %s %s: %s spread:%s" % (current_team, team_score, other_team, otherteam_score, spread,)

		game = dict()
		game['team'] = current_team
		game['other_team'] = other_team
		game['team_score'] = team_score
		game['other_team_score'] = otherteam_score
		game['spread'] = spread

		yearly_games.append(game)
	
	total_set[filename] = yearly_games


pickle.dump(total_set, open("total_set.p","wb"))
