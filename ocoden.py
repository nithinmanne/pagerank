import math
import numpy as np
from matplotlib import pyplot as plt 
import networkx
class PageRank:
	def __init__(self,graph=networkx.DiGraph(),d=0.85,epsilon=0.0001):
		self.graph=graph.copy()
		self.V=len(self.graph)
		self.d=d
		self.epsilon=epsilon
		self.ranks=dict()
		self.prhist=[]
		self.rlow=0
		self.nranks=dict()
		self.change=1.0
		self.initpr()
	def euclideanNorm(self,dic1,dic2,index):
		return math.sqrt(float(sum((dic1.get(d)-dic2.get(d))**2 for d in index)))
	def initpr(self):
		for node in self.graph:
			self.ranks[node]=1/float(self.V)
		i=0
		outll=dict()
		for n in self.graph: outll[n]=len(self.graph.out_edges(n))
		for i in xrange(1000):
			oldranks=self.ranks.copy()
			for node in self.graph.nodes():
				rank_sum=0
				for n in self.graph.predecessors(node):
					outlinks=outll[n]
					rank_sum+=(1/float(outlinks))*self.ranks[n]
				self.ranks[node]=((1-float(self.d))*(1/float(self.V)))+self.d*rank_sum
			if self.euclideanNorm(self.ranks,oldranks,self.graph)<self.epsilon: break
		ans=self.ranks.copy()
		psm=sum(ans[d] for d in ans)
		for d in ans: ans[d]/=psm
		self.prhist.append(ans)
		print "Number of Iterations : {}".format(i)
	def addgraph(self,graph):
		vchanged=set()
		vunchanged=set()
		for node in graph:
			vchanged.add(node)
		for node in self.graph:
			vunchanged.add(node)
		vunchanged=vunchanged.difference(vchanged)
		self.graph.add_edges_from(graph.edges())
		vpagerank=set()
		while(len(vchanged)!=0):
			n=vchanged.pop()
			if n in vpagerank: continue
			vpagerank.add(n)
			for i in self.graph.successors(n):
				vunchanged.discard(i)
				vchanged.add(i)
		for node in vunchanged:
			self.ranks[node]=self.ranks[node]*self.V/(len(self.graph))
		self.V=len(self.graph)
		vborder=set()
		for node in vpagerank:
			for node1 in self.graph.predecessors(node):
				vborder.add(node1)
		vborder=vborder.difference(vpagerank)
		for node in vborder:
			self.ranks[node]=self.ranks[node]*self.V/(len(vpagerank))
		print "Number of Changed Nodes : {}".format(len(vpagerank))
		print "Total Nodes : {}".format(len(self.graph))
		self.change=len(vpagerank)/float(len(self.graph))
		for node in vpagerank:
			self.ranks[node]=1/float(len(vpagerank))
		i=0
		nvpg=len(vpagerank)
		outll=dict()
		for n in vpagerank: outll[n]=len(self.graph.out_edges(n))
		for n in vborder: outll[n]=len(self.graph.out_edges(n))
		for i in xrange(1000):
			oldranks=self.ranks.copy()
			for node in vpagerank:
				rank_sum=0
				for n in self.graph.predecessors(node):
					outlinks=outll[n]
					rank_sum+=(1/float(outlinks))*self.ranks[n]
				self.ranks[node]=((1-float(self.d))*(1/float(nvpg)))+self.d*rank_sum
			if self.euclideanNorm(self.ranks,oldranks,vpagerank)<self.epsilon: break
		print "Number of Iterations : {}".format(i)
		#psm=sum(self.ranks[d] for d in vpagerank) for node in vborder: psm=psm+self.ranks[node] for d 
		#in vpagerank: self.ranks[d]/=psm
		for node in vborder:
			self.ranks[node]=self.ranks[node]*(len(vpagerank))/self.V
		for node in vpagerank:
			self.ranks[node]=self.ranks[node]*(len(vpagerank))/self.V
		ans=self.ranks.copy()
		su=sum(ans[n] for n in ans)
		for n in ans: ans[n]/=su
		self.prhist.append(ans)
	def normalized_pagerank(self):
		danglingnodes=[n for n in self.graph if self.graph.out_degree(n)==0.0]
		self.rlow=0
		print danglingnodes
		l=len(self.prhist)-1
		for n in danglingnodes:
			self.rlow+=self.prhist[l][n]
		self.rlow*=self.d
		self.rlow+=1-self.d
		self.rlow/=self.V
		for n in self.prhist[l]: self.nranks[n]=self.prhist[l][n]/self.rlow
	def printgraph(self,node):
                x=xrange(0,len(self.prhist))
                y=[]
                for i in x:
                        if node in self.prhist[i]: y.append(self.prhist[i][node])
                        else : y.append(0)
                plt.plot(x,y)
                plt.show()
	def printnormgraph(self,node):
		x=xrange(0,len(self.prhist))
                y=[]
                for i in x:
                        if node in self.prhist[i]: y.append(len(self.prhist[i])*self.prhist[i][node])
                        else : y.append(0)
                plt.plot(x,y)
                plt.show()
	def exppagerank(self,node,a):
		i=len(self.prhist)-1
		exp=1.0
		num=0.0
		den=0.0
		while i>=0:
			if node in self.prhist[i]: num+=exp*self.prhist[i][node]
			else: num+=0
			den+=exp
			exp/=math.exp(a)
			i-=1
		ans=num/den
		return ans
	def logpagerank(self,node,a):
                i=len(self.prhist)-1
                num=0.0
                den=0.0
                while i>=0:
			log=math.log(1+i*a)
                        if node in self.prhist[i]: num+=log*self.prhist[i][node]
                        else: num+=0
                        den+=log
                        i-=1
                ans=num/den
                return ans
	def predict_pagerank1(self,node,x,i=-1):
		a=[]
		if i==-1: i=len(self.prhist)-1
		count=0
		while count<x and i>=0:
			if node in self.prhist[i]:a.append(1000*self.prhist[i][node])
			else: a.append(0)
			i-=1
			count+=1
		b=[]
		for j in xrange(1,count+1):
		   b.append(j)
		c=np.polyfit(b,a,2)
		p=np.poly1d(c)
		return p(0)/1000.0
        def predict_pagerank2(self,node,x,i=-1):
                a=[]
		if(i==-1): i=len(self.prhist)-1
		k=i
		count=0
                while count<x and i>=1:
                        if node in self.prhist[i-1]:a.append(1000*(self.prhist[i][node]-self.prhist[i-1][node]))
                        else:
				if node in self.prhist[i]: a.append(1000*self.prhist[i][node])
				else: a.append(0)
                        i-=1
			count+=1
                b=[]
                for j in xrange(1,count+1):
                   b.append(j)
                c=np.polyfit(b,a,2)
                p=np.poly1d(c)
		if node in self.prhist[k]: return p(0)/1000.0
		return self.prhist[k][node]+p(0)/1000.0
