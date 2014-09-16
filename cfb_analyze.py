import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pickle 
import operator
import pylab 
import math

def main():

	data = pickle.load(open("total_set.p","rb"))

	team_set = set()
	for year in data:
		games = data[year]
		for game in games:
			team_set.add(game['team'])

	loss_ratio = dict()
	wins = dict()
	losses = dict()
	for team in team_set:
		wins[team], losses[team], loss_ratio[team] = pointspread_loss_ratio(data, team)
		#print "team: %s %s" % (team, loss_ratio[team])

	sorted_loss_ratio = sorted(loss_ratio.iteritems(), key=operator.itemgetter(1))
	for lr in sorted_loss_ratio:
		print "%s %s" % (lr[0], lr[1],)

	clean_loss_ratio_list = [ r for r in loss_ratio.values() if r != None ]

	print "mean: %s std: %s" % (np.mean(clean_loss_ratio_list), np.std(clean_loss_ratio_list))

	fig = pylab.figure()
	pylab.hist(clean_loss_ratio_list)
	fig.savefig("/home/kdrew/public_html/test/cfb_loss_ratio.pdf")
	#pylab.show()

	total_games = []
	win_percent = []
	team_list = []
	fig2, ax = pylab.subplots()
	for team in team_set:
		if wins[team] == None or losses[team] == None:
			continue
		total_games.append(wins[team]+losses[team])
		win_percent.append(1.0-loss_ratio[team])
		team_list.append(team)

	#ax.scatter(total_games, win_percent, marker='.', s=10)
	for i, team in enumerate(team_list):
		if team == "IOWA":
			ax.annotate(team, (total_games[i], win_percent[i]), fontsize=3, weight="extra bold")
		else:
			ax.annotate(team, (total_games[i], win_percent[i]), fontsize=2)

	ax.set_xlim(0.0,140.0)
	ax.set_ylim(0.55,1.0)
	ax.set_xlabel("number of games")
	ax.set_ylabel("winning percentage")

	ax.set_title("Double digit spread winning percentage since '99")
	fig2.savefig("/home/kdrew/public_html/test/cfb_doubledigit_spread_scatter.pdf")

	

	#pointspread_loss_ratio(data, 'IOWA')
	#pointspread_loss_ratio(data, 'MICHIGAN')
	#pointspread_loss_ratio(data, 'OHIO STATE')
	#pointspread_loss_ratio(data, 'PENN STATE')
	#pointspread_loss_ratio(data, 'MINNESOTA')
	#pointspread_loss_ratio(data, 'MICHIGAN STATE')
	#pointspread_loss_ratio(data, 'INDIANA')
	#pointspread_loss_ratio(data, 'NORTHWESTERN')
	#pointspread_loss_ratio(data, 'WISCONSIN')
	#pointspread_loss_ratio(data, 'PURDUE')
	#pointspread_loss_ratio(data, 'ILLINOIS')
	#pointspread_loss_ratio(data, 'NEBRASKA')
	#pointspread_loss_ratio(data, 'ALABAMA')
	#pointspread_loss_ratio(data, 'LSU')

def pointspread_loss_ratio(data, team, spread=-10.0, numGamesThreshold=15.0):

	wins = 0.0
	losses = 0.0
	for year in data:
		games = data[year]
		for game in games:
			if game['spread'] <= spread:
				#if 'IOWA' in game['team'] and 'STATE' not in game['team']:
				#if 'MINNESOTA' in game['team'] and 'STATE' not in game['team']:
				if team == game['team']:
					if game['team_score'] > game['other_team_score']:
						#print "WON: %s" % (game,)
						wins += 1.0
					else:
						#print "LOSS: %s" % (game,)
						losses += 1.0

	if wins + losses < numGamesThreshold:
		return None,None,None

	loss_ratio = losses / (wins + losses)
	print "team: %s wins: %s losses: %s loss ratio: %s" % (team, wins, losses, loss_ratio,)
	return wins, losses, loss_ratio

if __name__ == "__main__":
	main()

