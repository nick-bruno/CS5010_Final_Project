## Homework 3: Python (Webscraping)

	# By: Nick Bruno and Justin Niestroy
	# Computing ids: nhb3zf, jcn4rh

import requests #used https://www.dataquest.io/blog/web-scraping-tutorial-python/ for help
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt # Allows us to create interesting plots
import numpy as np
import statsmodels.api as sm
def PGA_Stats(url):
	page = requests.get(url)
	# page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page.content,"html5lib")
	#print(soup.prettify())
	csv = ''
	n = 1
	for th in soup.find_all('th'):
		csv += (th.text.replace(' ','') + ',')
	csv += '\n'
	for tr in soup.find_all('tr'): #got help from https://www.dataquest.io/blog/web-scraping-tutorial-python/
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
plt.show()  # Here is plot if you want to show this uncomment 

points = df[['PLAYERNAME','POINTS']] # creates a dataset with playername and their points

average_points = np.mean(points['POINTS'])
# print(average_points)
	# average amount of points per player

ntotal = len(points)
# print(ntotal)
	# finds total number of golfers in the dataset

maxpoints = np.max(points['POINTS'])
# print(maxpoints) 
	# finds maximum number of fedex points
minpoints = np.min(points['POINTS'])
# print(minpoints)
	# finds minimum number of fedex points
stdpoints = np.std(points['POINTS'])
# print(stdpoints)
	# finds standard deviation of fedex points

midpoint = maxpoints//2
	# finds midpoint of golfers in our dataset
closegolfers = points[points.POINTS >= midpoint] # looks at golfers 'close' to Dustin Johnson
ncloser = len(closegolfers)
	# Number of golfers 'close' to Dustin Johnson
nfarther = ntotal - ncloser
	# Number of golfers with less than 1006 points
propclose = (ncloser/ntotal) * 100
	# finds proportion of golfers close to first place
lowpoints = points[points.POINTS <= 10] # subsets to golfers who have 10 or less points
nlowpoints = len(lowpoints)
	# 24 golfers have 10 points of less

df['Rankingdiff'] = df['RANKTHISWEEK'] - df['RANKLASTWEEK'] # creates new column looking at the differnce in rankings between the weeks
df['absRankingdiff'] = df['Rankingdiff'].abs()
ranks = df[['PLAYERNAME', 'Rankingdiff', 'absRankingdiff']] # condences datasete so that there is only player name and rankingdiff
sortedranks = ranks.sort_values(by=['Rankingdiff']) # source https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.sort.html
	# sorts the golfers by their ranking difference from the current week compared to the previous week
average_rank_change = np.mean(ranks['absRankingdiff'])
	# finds average movement in rankings
maxranks = np.max(ranks['Rankingdiff'])
	# biggest improvement in ranking
minranks = np.min(ranks['Rankingdiff'])
	# worst fall in ranking
worstgolfer = sortedranks.iloc[0]
	# Prints the first observation which is the golfer and their difference
mostimproved = ranks[ranks.Rankingdiff == 5] # looks at the golfers with the highest jump in rankings
	# Ian Poulter and Emiliano Grillo  (5) are the most improved rankings wise

roundsdf = df1[['PLAYERNAME', 'ROUNDS']]

maxrounds = np.max(roundsdf['ROUNDS'])
	# finds greatest number of rounds played by a PGA golfer
minrounds = np.min(roundsdf['ROUNDS'])
	# finds the least amount of rounds played by a PGA golfer
avg_rounds = np.mean(roundsdf['ROUNDS'])
	# finds average rounds played by a PGA golfer
maxgolfers = roundsdf[roundsdf.ROUNDS == maxrounds]
	# finds golfer(s) with the most rounds played
maxgolfer_name = maxgolfers['PLAYERNAME']
	# finds the player's name
mingolfers = roundsdf[roundsdf.ROUNDS == minrounds]
	# finds golfer(s) with the most rounds played
mingolfer_name = mingolfers['PLAYERNAME']
	# find's the player's name


X1 = tot_df.filter(['SG:OTT'], axis=1)
Y = tot_df['POINTS']
X2 = tot_df['SG:APR']
X3 = tot_df['SG:ARG']
model_off_tee = sm.OLS(Y, X1).fit() # .OLS() source: https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
model_approach = sm.OLS(Y, X2).fit()
model_around_green = sm.OLS(Y, X3).fit()
#predictions = model.predict(X) # make the predictions by the model
# Print out the statistics
print(model_off_tee.summary())#R^2 is equal to .17
print(model_approach.summary())#R^2 is equal to .2
print(model_around_green.summary())#R^2 is equal to .076

# Easy access to the analysis in our report
print('Total golfers: ' + str(ntotal))
print('Maximum FedEx Points: ' + str(maxpoints))
print('Minimum FedEx Points: ' + str(minpoints))
print('Average FedEx Points: ' + str(average_points))
print('Standard Deviation of FedEx Points: ' + str(stdpoints))
print('Number of golfers we consider "close" to the leader: ' + str(ncloser))
print('Proportion of golfers we consider "close" to the leader: ' + str(propclose))
print('Number of golfers we consider "far" from the leader: ' + str(nlowpoints))
print('Average difference in golfer ranking from last week to current week: ' + str(average_rank_change))
print('The golfers with the greatest improvement in FedEx ranking: ' + '\n' + str(mostimproved))
print('The golfers with the worst difference in FedEx ranking: '+ '\n' + str(worstgolfer))
print('Average rounds of golf played by a PGA golfer: ' + str(avg_rounds))
print('Most rounds of golf played by a PGA golfer: ' + str(maxrounds))
print('Golfer with the most rounds of golf played: ' + '\n' + str(maxgolfer_name))
print('Least amount of rounds of golf played by a PGA golfer: ' + str(minrounds))
print('Golfer with the least amount rounds of golf played: ' + '\n' + str(mingolfer_name))


### Sources used ###
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
# https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.sort.html
# https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.OLS.html
