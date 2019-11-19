#! /usr/bin/python3

import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


#read employee list
authorsList=[]
authorsFile=open('ut_chem_employees.csv','r', encoding='utf-8-sig')
for line in authorsFile:
	line=line.rstrip()
	author=line.split(',')[0]
	#add author node
	authorsList.append(author)
authorsFile.close()

authorsFromArticles=[]
#read articles list and get all unique authors
articlesFile=open('ut_chem_publications.csv','r', encoding='utf-8-sig')
for line in articlesFile:
	lineList=line.split('"')
	#only look at papers from 2014 - to present
	year=lineList[2].lstrip(',')
	year=int(year)
	if year>=2015:
		#get array of authors
		authors=lineList[1].strip().split(' ; ')
		for i, name in enumerate(authors):
			authors[i]=name.replace(',', '')
		for name in authors:
			if name in authorsFromArticles:
				pass
			else:
				authorsFromArticles.append(name)
articlesFile.close()

#print("authors from employee list ", len(authorsList))
#print("authors from publications list ", len(authorsFromArticles))

summedNames=authorsList+authorsFromArticles
#remove possible duplicates
summedNames=list(dict.fromkeys(summedNames))


#get list of unique first names present in employee list
firstNames=[]
for name in summedNames:
	firstName=name.split(' ')[1]
	if firstName in firstNames:
		pass
	else:
		firstNames.append(firstName)

#remove possible duplicates
firstNames=list(dict.fromkeys(firstNames))

#read in csv file with estonian male names
maleNamesFile=open('mehenimed.csv', 'r',encoding='utf-8-sig')
for line in maleNamesFile:
	line.strip()
	lineList=line.split(',')
	if len(lineList)!=0:
		maleNames=lineList

#check if some first names have multiple last names (only check non-males)
for firstName in firstNames:
	nameList=[]
	for author in summedNames:
		if author.split(' ')[1]==firstName:
			if author.split(' ')[1] in maleNames:
				pass
			else:
				nameList.append(author)
	if len(nameList)>1:
		#for finding women with same first name - checking if more aliases are needed
		#print(nameList)
		pass
#create graph
G=nx.Graph()
#create nodes
authorsList=[]
authorsWithAliases=[]
authorsFile=open('ut_chem_employees.csv','r', encoding='utf-8-sig')
for line in authorsFile:
	line=line.rstrip()
	lineList=line.split(',')
	G.add_node(lineList[0],affiliation="chem", alias="None")
	if len(lineList)>1:
		G.node[lineList[0]]['alias']=lineList[1]
		print("aliases found", lineList)
		#store authors with aliases in list for later use
		authorsWithAliases.append([lineList[0],lineList[1]])
	#add author node
	authorsList.append(author)
authorsFile.close()
#print(list(G.nodes(data=True)))

#create list of articles (filtered, parsed)
articlesList=[]
articlesFile=open('ut_chem_publications.csv','r', encoding='utf-8-sig')
for line in articlesFile:
	lineList=line.split('"')
	#get array of authors
	authors=lineList[1].strip().split(' ; ')
	for i, name in enumerate(authors):
		authors[i]=name.replace(',', '')
	#get publication year	
	year=int(lineList[2].split(',')[1])
	#add publication to articlesList if year >=2015
	if year >= 2015:
		articlesList.append([authors,year])
articlesFile.close()
#print(articlesList)

#replace aliases in publication name fields with current name
for authorName in authorsWithAliases:
	correctName=authorName[0]
	alias=authorName[1]
	print("correct",correctName,"alias",alias)
	#iterate over each article
	for article in articlesList:
		for i in range(len(article[0])):
			if article[0][i]==alias:
				article[0][i]=correctName
				print("replaced",alias)

#create edges
for article in articlesList:
	#iterate over all possible combinations of authors
	for i in range(0, len(article[0])-1):
		for j in range(i+1, len(article[0])):
			pass
			if G.has_node(article[0][i])==True and G.has_node(article[0][j])==True:
				#found potential edge, check if already present
				if G.has_edge(article[0][i],article[0][j])==True:
					#edge present, change count
					G.edges[article[0][i],article[0][j]]['count']=G.edges[article[0][i],article[0][j]]['count']+1
				else:
					#edge not found, add new
					G.add_edge(article[0][i],article[0][j],count=1)

#initial nodes and edges are finished

#find isolates (nodes with no edges)
isolates=list(nx.isolates(G))
G.remove_nodes_from(isolates)					

#calculate degree centrality and print ordered
degreeCentrality=nx.degree_centrality(G)
for key,value in sorted(degreeCentrality.items(), key=itemgetter(1), reverse=True):
	print(key,value)

nx.draw_networkx(G,pos=nx.spring_layout(G,weight='count'), node_size=10, edge_color='green', font_size=7)
nx.write_gexf(G, 'test.gexf')
plt.show()
