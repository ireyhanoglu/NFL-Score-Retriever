import urllib2
import json

#Get teams' abbreviation and name (32 NFL teams total)
def get_abbr_and_name(nfl_teams,nfl_teams_list):
	i=0
	while(i<32):
		team_abbreviation=nfl_teams['teams'][i]['abbr']
		team_name=nfl_teams['teams'][i]['nick']
		nfl_teams_list[team_abbreviation]=team_name
		i+=1
	return nfl_teams_list

#Get NFL teams' abbreviation and team name
def get_nfl_teams_info():
	#Capture teams' info from website json
	nfl_teams_json_website='http://feeds.nfl.com/feeds-rs/teams/2016.json'
	output=urllib2.urlopen(nfl_teams_json_website).read()

	#Dump teams' info to a team info file
	nfl_teams_json='nfl_teams.json'
	f=open(nfl_teams_json,'w')
	f.write(output)
	f.close()

	#Open file with teams' info
	with open(nfl_teams_json) as data:    
	    nfl_teams = json.load(data)

	#Will contain teams' abbreviation and name
	nfl_teams_list={}

	return get_abbr_and_name(nfl_teams,nfl_teams_list)

