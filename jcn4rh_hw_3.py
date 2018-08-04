#import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def PGA_Stats(url):
	page = requests.get(url)
	#page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.content,"html5lib")
	#print(soup.prettify())
	csv = ''
	n = 1
	for th in soup.find_all('th'):
		csv += (th.text.replace(' ','') + ',')
	csv += '\n'
	for tr in soup.find_all('tr'):
		if "class" in tr.attrs and tr.attrs['class'][0] == 'hidden-small':
			continue
		if n  < 3: #to format csv
			n += 1
			continue
		for td in tr.find_all('td'):
			csv += (td.text.replace("\n","").replace(",","").replace(' ','').replace('\xa0','') + ',').strip() # has random new line in some data where we dont want so remove unwanted new lines
		csv += '\n'
	return(csv)
#these files are in same directory already so don't want to redownload everytime we run script

pga = 'http://www.pgatour.com/fedexcup/official-standings.html'
pga2 = 'https://www.pgatour.com/stats/stat.02674.html'
f = open("PGA_Stats_Fed_ex_June_24.csv","w")
f.write(PGA_Stats(pga))
f.close()
f = open("PGA_Stats_stokes_gained_June_24.csv","w")
f.write(PGA_Stats(pga2))
f.close()
df = pd.read_csv('PGA_Stats_Fed_ex_June_24.csv',encoding = "ISO-8859-1")
df1 = pd.read_csv('PGA_Stats_stokes_gained_June_24.csv',encoding = "ISO-8859-1")
df = df.sort_values(by = ['PLAYERNAME'])
df1.sort_values(by= ['PLAYERNAME'])
tot_df = df1.merge(df, on = 'PLAYERNAME',how = 'left')
tot_df = tot_df.fillna(0)
tot_df.loc[tot_df["#OFTOP10'S"] == '--', "#OFTOP10'S"] = 0
tot_df["#OFTOP10'S"] = pd.to_numeric(tot_df["#OFTOP10'S"])*1.0
# print(tot_df["#OFTOP10'S"])
# tot_df.to_csv('total.csv')
# tot_df.plot.scatter(x='AVERAGE', y='RANKTHISWEEK_y')
# plt.show()
# tot_df.plot.scatter(x='AVERAGE', y='POINTS',s=tot_df["#OFTOP10'S"]*10)
# plt.show()
cm = plt.get_cmap('GnBu')#GnBu looks nice OrRd also was cool
tot_df.plot.scatter(x='AVERAGE', y='POINTS',c=tot_df["#OFTOP10'S"]*.1,s=50,cmap = cm)
plt.show()


df = pd.read_csv('PGA_Stats_Fed_ex_June_24.csv')
dfstats = pd.read_csv('PGA_Stats_stokes_gained_June_24.csv')
x =df['PLAYERNAME']
	# this works boiii

points = tot_df[['PLAYERNAME','POINTS']] # creates a dataset with playername and their points
print(points)
y = np.mean(points)
	# average amount of points per player is 425.293436

ntotal = len(x)
	# 259 total golfers

maxpoints = np.max(points)
	# max points is 2013

midpoint = 2013/2
closegolfers = points[points.POINTS > midpoint] # looks at golfers 'close' to Dustin Johnson
ncloser = len(closegolfers)
	# Only 26 golfers are within half the amount of points as Dustin Johnson right now

nfarther = ntotal - ncloser
	# 232 golfers are 'well behind' (less than 1/2 the points) compared to Dustin Johnson

propclose = (ncloser/ntotal) * 100
	# Only 10.424710424710424% of golfers are close to catching Dustin Johnson

df['Rankingdiff'] = df['RANKTHISWEEK'] - df['RANKLASTWEEK'] # creates new column looking at the differnce in rankings between the weeks

ranks = df[['PLAYERNAME', 'Rankingdiff']] # condences datasete so that there is only player name and rankingdiff
sortedranks = ranks.sort_values(by=['Rankingdiff'])
worstgolfer = sortedranks.iloc[0]
	# Prints the first observation which is the golfer and their difference (Bernhard Langer (-26)) (only one)
mostdigress = ranks[ranks.Rankingdiff == -26]
bestgolfer = sortedranks.iloc[len(sortedranks) - 1] # takes the last row of the data (highest improvement)
	# Ian Poulter (5) (might be multiple)
mostimproved = ranks[ranks.Rankingdiff == 5] # looks at the golfers with the highest jump in rankings
print(mostimproved)
	# Ian Poulter and Emiliano Grillo  (5) are the most improved rankings wise
maxranks = np.max(ranks)
	# someone moved up 5 spots
minranks = np.min(ranks)
	# someone dropped 26 spots
pointssorted = points.sort_values(by=['POINTS'])
print(pointssorted)

lowpoints = points[points.POINTS <= 10] # subsets to golfers who have 10 or less points
nlowpoints = len(lowpoints)
	# 24 golfers have 10 points of less


## Looking at dfstats ##
roundsdf = tot_df[['PLAYERNAME', 'ROUNDS']]
print(roundsdf)

maxrounds = np.max(roundsdf)
	# 93 is highest number of rounds played by a player
minrounds = np.min(roundsdf)
	# 36 is lowest number of rounds played by a player

