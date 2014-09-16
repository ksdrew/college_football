import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pickle 
import operator
import pylab 

def main():

	data = pickle.load(open("total_set.p","rb"))

	team_set = set()
	for year in data:
		games = data[year]
		for game in games:
			team_set.add(game['team'])

	win_percent = dict()
	numOfgames = dict()
	for team in team_set:
		win_percent[team], numOfgames[team] = closegame_winning_percentage(data, team)
		#print "team: %s %s" % (team, win_percent[team])

	sorted_win_percent= sorted(win_percent.iteritems(), key=operator.itemgetter(1))
	for lr in sorted_win_percent:
		print "%s %s" % (lr[0], lr[1],)

	clean_win_percent_list = [ r for r in win_percent.values() if r != None ]

	print "mean: %s std: %s" % (np.mean(clean_win_percent_list), np.std(clean_win_percent_list))

	fig = pylab.figure()
	pylab.hist(clean_win_percent_list)
	fig.savefig("/home/kdrew/public_html/test/cfb_close_games.pdf")
	#pylab.show()
	
	total_games = []
	win_percent_list = []
	team_list = []
	fig2, ax = pylab.subplots()
	for team in team_set:
		if numOfgames[team] == None or win_percent[team]==None:
			continue
		total_games.append(numOfgames[team])
		win_percent_list.append(win_percent[team])
		team_list.append(team)

	#ax.scatter(total_games, win_percent, marker='.', s=10)
	for i, team in enumerate(team_list):
		if team == "IOWA":
			ax.annotate(team, (total_games[i], win_percent_list[i]), fontsize=3, weight="extra bold")
		else:
			ax.annotate(team, (total_games[i], win_percent_list[i]), fontsize=2)

	ax.set_xlim(10.0,85.0)
	ax.set_ylim(0.3,0.75)
	ax.set_xlabel("number of games")
	ax.set_ylabel("winning percentage")

	ax.set_title("Winning percentage of games less than 7pts since '99")
	fig2.savefig("/home/kdrew/public_html/test/cfb_closegames_scatter.pdf")



def closegame_winning_percentage(data, team, closeness=7.0, numGamesThreshold=15.0):

	wins = 0.0
	losses = 0.0
	for year in data:
		games = data[year]
		for game in games:
			if game['team_score'] != None and game['other_team_score'] != None:
				if abs(game['team_score'] - game['other_team_score']) <= closeness:
					if team == game['team']:
						if game['team_score'] > game['other_team_score']:
							#print "WON: %s" % (game,)
							wins += 1.0
						else:
							#print "LOSS: %s" % (game,)
							losses += 1.0

	if wins + losses < numGamesThreshold:
		return None, None

	win_percent = wins / (wins + losses)
	print "team: %s wins: %s losses: %s winning percentage: %s" % (team, wins, losses, win_percent,)
	return win_percent, (wins + losses)

if __name__ == "__main__":
	main()

