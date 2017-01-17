import urllib2
import json
from collections import OrderedDict

def get_current_nfl_week_scores():
	live_scores='http://www.nfl.com/liveupdate/scores/scores.json'

	output=urllib2.urlopen(live_scores).read()

	scores_file='scores.txt'

	f=open(scores_file,'w')
	f.write(output)
	f.close()

	with open(scores_file) as data:    
		    live_nfl_scores = json.load(data)

	live_nfl_scores=json.dumps(live_nfl_scores,indent=4,sort_keys=True)

	f=open(scores_file,'w')
	f.write(live_nfl_scores)
	f.close()

	lines=[]
	sym='201' #Games between teams are labeled by their date, all start with the year 201_
	with open(scores_file) as f:
	    for line in f:
	        lines.append(line)

	team_and_score=OrderedDict()

	live_nfl_scores = json.loads(live_nfl_scores)
	for line in lines:
		score=''
		if sym in line:
			before_date_split=line.split('":',1)
			score=before_date_split[0]
			after_date_split=score.split('"',1)
			score=after_date_split[-1]
			team_and_score[ live_nfl_scores[score]['away']['abbr'] ] = live_nfl_scores[score]['away']['score']['T']
			team_and_score[ live_nfl_scores[score]['home']['abbr'] ] = live_nfl_scores[score]['home']['score']['T']
			if team_and_score[ live_nfl_scores[score]['away']['abbr'] ] == None:
				team_and_score[ live_nfl_scores[score]['away']['abbr'] ] = '--'
			if team_and_score[ live_nfl_scores[score]['home']['abbr'] ] == None:
				team_and_score[ live_nfl_scores[score]['home']['abbr'] ] = '--'

	del lines

	return team_and_score