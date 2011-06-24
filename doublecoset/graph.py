#Labelled vertex, with labelled edges.
#edges are doubles (label, vertex)
import os

class Vertex:
	def __init__(self,label):
		self.label = label
		self.outedges = []
		self.inedges = []

	def __repr__(self):
		return str(self)

	def __str__(self):
		return 'v'+str(self.label)

	def addInEdge(self,label,v):
		if not (label,v) in self.inedges:
			self.inedges.append((label,v))

	def addOutEdge(self,label,v):
		if not (label,v) in self.outedges:
			self.outedges.append((label,v))

	def getFolds(self):
		outfolds = {}
		for label, v in self.outedges:
			if not label in outfolds:
				outfolds[label] = []
			outfolds[label].append(v)

		outfolds = [(label,vs) for label,vs in outfolds.items() if len(vs)>1]

		infolds = {}
		for label, v in self.inedges:
			if not label in infolds:
				infolds[label] = []
			infolds[label].append(v)

		infolds = [(label.upper(),vs) for label,vs in infolds.items() if len(vs)>1]

		return outfolds+infolds


#A general graph object
#not necessarily connected
class Graph:
	vertexCount = 0	#accumulator for labelling vertices

	def __init__(self):
		self.vertices = []
	
	#create a new vertex in the graph, and return it
	def addVertex(self):
		self.vertexCount += 1
		v=Vertex(self.vertexCount)
		self.vertices.append(v)
		return v
	
	#merge vertices u and v, removing v from the graph
	def mergeVertices(self,u,v):
		if u==v: return

		self.vertices.remove(v)
		for label,w in v.outedges:			#for each labelled edge v->w
			w.inedges.remove((label,v))		#remove edge from w's list of in-edges
			w.addInEdge(label,u)			#add an edge u->w to w's in-edges
			u.addOutEdge(label,w)			#add "			" to u's out-edges

		for label,w in v.inedges:			#for each labelled edge joining w->v
			w.outedges.remove((label,v))	#remove edge from w's list of out-edges
			w.addOutEdge(label,u)			#add an edge w->u to w's out-edges
			u.addInEdge(label,w)			#add "			" to u's in-edges

		return u
	
	#add a labelled edge u->v
	#lower-case labels are forwards edges
	#upper-case labels are backwards edges
	def addEdge(self,u,v,label):
		if label==label.lower():		
			u.addOutEdge(label,v)
			v.addInEdge(label,u)
		else:
			self.addEdge(v,u,label.lower())	

	#add a labelled circle rooted at u, so reading round edge labels gives word
	def addLoop(self,u,word):
		root = u
		for c in word[:-1]:				#for each letter in the word:
			v = self.addVertex()		#create a new vertex
			self.addEdge(u,v,c)			#add a labelled edge connecting previous vertex to the new one
			u=v

		self.addEdge(u,root,word[-1])	#add a final edge connecting back to the root, with label the last letter of the word
	
	#fold the graph once
	#that is: any number of vertices might be merged, but each vertex will be merged at most once
	def fold(self):
		folds = sum([v.getFolds() for v in self.vertices],[])	#get all possible folds
		folded = []												#keep track of which vertices have been folded

		for label,vs in folds:							#for each possible fold
			vs = [v for v in vs if not v in folded]		#remove vertices that have been involved in a previous fold
			if len(vs)>1:								#if there are still vertices to be folded
				u=vs[0]									#the first vertex in the list, u, will be the one that survives
				folded.append(u)						#add u to the list of vertices not to merge again
				for v in vs[1:]:						#for each other vertex v in this fold
					self.mergeVertices(u,v)				#merge it with u
					folded.append(v)					#add v to the list of vertices not to merge again

		return len(folds)>0								#return true if any folds took place

	def graphViz(self,name='G'):
		out = []
		for u in self.vertices:
			out.append('%s%s [shape=point];' % (name,u))
			for label,v in u.outedges:
				out.append( '%s%s -> %s%s [label="%s"];' % (name,u,name,v,label) )
		return '\n'.join(out)
	
	def __str__(self):
		return self.graphViz('G')

#little demo/test
def _test_():
	g=Graph()
	v=g.addVertex()
	g.addLoop(v,'abAB')
	g.addLoop(v,'abC')
	g.addLoop(v,'adbC')
	out = '';
	step = 0
	out = g.graphViz('g'+str(step))
	go = True
	while go:
		step += 1
		out = g.graphViz('g'+str(step))
		out = 'digraph {\n%s\n}' % out
		open('test%s.gv' % step,'w').write(out)
		os.system('neato -Tpng test%s.gv > test%s.png' % (step,step))
		go = g.fold()

if __name__=='__main__':
	_test_()
