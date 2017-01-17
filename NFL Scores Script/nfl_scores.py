import subprocess
import urllib2
import nfl_teams, current_week_nfl_scores
from collections import OrderedDict

def nfl_scores(nfl_teams):

	def get_scores(week_number,scores_file):
		nfl_website='http://www.nfl.com/scores/2016/REG' + week_number

		output=urllib2.urlopen(nfl_website).read()

		f=open(scores_file,'w')
		f.write(output)
		f.close()

	def get_scores_post(week_number,scores_file):
		nfl_website='http://www.nfl.com/scores/2016/POST' + week_number

		output=urllib2.urlopen(nfl_website).read()

		f=open(scores_file,'w')
		f.write(output)
		f.close()

	# To check if the week number entered by the user is the current NFL week
	def is_current_week(week_number,scores_file):
		nfl_week=''
		with open(scores_file) as lines:
			for line in lines:
				if '<title>NFL Scores: 2016 - Wild Card' in line:
					nfl_week=str(18)
				elif '<title>NFL Scores: 2016 - Divisional' in line:
					nfl_week=str(19)
				elif '<title>NFL Scores: 2016 - Conference' in line:
					nfl_week=str(20)
				elif '<title>NFL Scores: 2016 - Super Bowl' in line:
					nfl_week=str(22)
				elif '<title>NFL Scores: 2016' in line:
					before_week_split=line.split('<title>NFL Scores: 2016 - Week ',1)
					nfl_week=before_week_split[-1]
					after_week_split=nfl_week.split('<',1)
					nfl_week=after_week_split[0]
		return (nfl_week==week_number)

	def assign_score_to_team(team_and_score,nfl_teams,line_number):
		lines=[]
		with open(scores_file) as f:
		    for line in f:
		        lines.append(line)
		for line in lines:
			if ('<p class="total-score">' in line):
				before_score_split=line.split('">',1)
				score=before_score_split[-1]
				after_score_split=score.split('<',1)
				score=after_score_split[0]

				line_of_team=lines[line_number-2]
				team=''
				for abbr in nfl_teams.keys():
					if(abbr in line_of_team):
						team=abbr
				team_and_score[team]=score
			line_number+=1
		
		del lines
		return team_and_score

# /////////////////////////////////////////////////////////////////////
# main code

	nfl_teams=nfl_teams.get_nfl_teams_info()
	scores_file='scores.txt'
	line_number=0 #actual line number is line_number+1
	team_and_score=OrderedDict()
	individual_game=1
	week_number=raw_input("Enter the week for NFL scores, or press Enter for this week's scores: ")
	
	if week_number=='': #press enter for current week scores
		team_and_score=current_week_nfl_scores.get_current_nfl_week_scores()
	
	elif int(week_number)<18: #regular season scores
		get_scores('',scores_file)
		if (is_current_week(week_number,scores_file)==False):
			get_scores(week_number,scores_file)
			team_and_score=assign_score_to_team(team_and_score,nfl_teams,line_number)
		else:
			team_and_score=current_week_nfl_scores.get_current_nfl_week_scores()
	
	else: #post season scores
		get_scores('',scores_file)
		if (is_current_week(week_number,scores_file)==False):
			get_scores_post(week_number,scores_file)
			team_and_score=assign_score_to_team(team_and_score,nfl_teams,line_number)
		else:
			team_and_score=current_week_nfl_scores.get_current_nfl_week_scores()

	for team, score in team_and_score.items():
		print '%s: %s' % (team,score)
		if( (individual_game % 2) == 0):
			print ''
		individual_game+=1

nfl_scores(nfl_teams)







