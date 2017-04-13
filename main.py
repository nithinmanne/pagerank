import networkx
import ocoden
import time
from matplotlib import pyplot
from random import randint
import sys
import os

def test(filename=None,parts=100,esc=" "):
	f=open(filename)
	i=0
	for l in f:
		i=i+1
	n=i/parts
	g=networkx.DiGraph()
	f=open(filename)
	i=0
	for l in f:
		i=i+1
		a=l.strip().split(esc)
		g.add_edge(int(a[0]),int(a[1]))
		if i==n: break
	t=time.time()
	cl=ocoden.PageRank(g)
	print "Time for Initial Page Rank : {}".format(time.time()-t)
	g.clear()
	j=0
	i=0
	x=[]
	y=dict()
	for l in f:
		i=i+1
		if i==n:
			j+=1
			i=0
			print "Part : {}".format(j)
			t=time.time()
			cl.addgraph(g)
			t1=time.time()-t
			print "Time for Inc. Page Rank : {}".format(t1)
			t=time.time()
			cl1=ocoden.PageRank(cl.graph)
			t2=time.time()-t
			print "Time for Full Page Rank : {}".format(t2)
			x.append(cl.change)
			y[cl.change]=t2/t1
			norm=cl.euclideanNorm(cl.prhist[len(cl.prhist)-1],cl1.prhist[0],cl.graph)
			print "Euclidean Norm between these two results : {}".format(norm)
		a=l.strip().split(esc)
		g.add_edge(int(a[0]),int(a[1]))
	x.sort()
	ys=[y[n] for n in x]
	#pyplot.ion()
	pyplot.figure("Times Faster vs. Change")
	pyplot.xlabel("Percentage of Change")
	pyplot.ylabel("Times Faster")
	pyplot.plot(x,ys,"o")
	#pyplot.ioff()
	try:
		os.stat("figs")
	except:
		os.mkdir("figs")
	pyplot.savefig("figs/time.png")
	pyplot.close('all')
	nodes=cl.graph.nodes()
	l=len(nodes)-1
	if l<500: return
	node=set()
	for i in range(50):
		rand=0
		while True:
			rand=randint(0,l)
			if rand in node: continue
			node.add(rand)
			break
		pyplot.figure("Node {}".format(nodes[rand]))
		x=xrange(0,len(cl.prhist))
		y=[]
		for i in x:
			if nodes[rand] in cl.prhist[i]: y.append(cl.prhist[i][nodes[rand]])
			else : y.append(0)
		pyplot.plot(x,y,label="Actual Page Rank")
		x=xrange(2,len(cl.prhist))
		y1=[cl.predict_pagerank1(nodes[rand],5,i) for i in x]
		y2=[cl.predict_pagerank2(nodes[rand],5,i) for i in x]
		pyplot.plot(x,y1,label="Polynomial Prediction")
		pyplot.plot(x,y2,label="Differential Polynomial Prediction")
		eavg=cl.exppagerank(nodes[rand],1)
		lavg=cl.logpagerank(nodes[rand],1)
		pyplot.plot([0,len(cl.prhist)-1],[eavg,eavg],label="Exponential Average")
		pyplot.plot([0,len(cl.prhist)-1],[lavg,lavg],label="Logarithemic Average")
		pyplot.savefig("figs/{}.png".format(nodes[rand]))
		pyplot.close('all')
	
def run(filename=None,parts=10,esc=" "):
	f=open(filename)
        i=0
        for l in f:
                i=i+1
        n=i/parts
        g=networkx.DiGraph()
        f=open(filename)
        i=0
        for l in f:
                i=i+1
                a=l.strip().split(esc)
                g.add_edge(int(a[0]),int(a[1]))
                if i==n: break
        cl=ocoden.PageRank(g)
        g.clear()
        j=0
        i=0
        for l in f:
                i=i+1
                if i==n:
                        j+=1
                        i=0
                        print "Part : {}".format(j)
                        cl.addgraph(g)
                a=l.strip().split(esc)
                g.add_edge(int(a[0]),int(a[1]))

if __name__== '__main__':
	if len(sys.argv) == 1:
		print "Expected input format: python main.py filename"
	else:
		filename=sys.argv[1]
		test(filename)
