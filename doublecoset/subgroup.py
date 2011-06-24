from graph import Graph
from word import *

#a folded subgroup graph
class subgroupGraph(Graph):
	#create a graph from a list of generators
	@classmethod
	def fromGenerators(self,words):
		g=subgroupGraph(rooted=True)
		for word in words:
			g.addLoop(g.root,word)
		while g.fold():
			pass
		return g

	#does word belong to this subgroup?
	#read the word along the graph, and if you end up back at the root vertex, then the word is in the subgroup
	def __contains__(self,word):
		word = freelyReduce(word)	#make sure word is freely reduced, just to save time
		v=self.root					#start at the root vertex
		for c in word:				#for each letter in the word
			if c==c.lower():		#lower case means x, upper case means x^{-1}
				es = v.outedges		#if x, we want an outward edge
			else:
				es = v.inedges		#if x^{-1}, we want an inward edge

			c=c.lower()
			if c in es:				#if there is an edge with the right label in the right direction
				v=es[c][0]			#move to the vertex it is pointing to
			else:
				return False		#otherwise, we can't go anywhere, so the word is not in the subgroup

		return v==self.root		#if we finish at the root vertex after reading the whole word, then the word is in the subgroup

#a simple test
def _test_():
	g = subgroupGraph.fromGenerators(['abAB','abC','adbC'])

	#try a few words to see if they're in the subgroup
	for word in ['abAB','a','cBA','abCaAcCdD']:
		if word in g:
			print('%s is in the subgroup' % word)
		else:
			print('%s is not in the subgroup' % word)


if __name__=='__main__':
	_test_()
