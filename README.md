# Page Rank for Evolving Graphs

The Page Rank for Evolving Graphs can be calculated using an Incremental Algorithm.

## Usage

The module ocoden.py implements a class PageRank which is initialized by:

```
PageRank(graph=networkx.DiGraph(),d=0.85,epsilon=0.0001)
```
This initializes the graph and also calculates the PageRank for the initial nodes and stores it. This is calculated using the normal power iteration method for computing PageRank. It checks for convergence using Euclidean Norm.

Arguments:

1. **graph**: This is the graph that is to be given for initialization. By default, it creates an empty graph and uses it if nothing is provided. Type: NetworkX DiGraph.
2. **d**: This is the damping factor that is used for calculating Page Rank. By default, it is set to 0.85. Type: float
3. **epsilon**: This is the threshold of convergence. If the Euclidean norm of the difference between the approximations of the steady state vector before and after an iteration of power iteration is smaller than epsilon, the algorithm will consider itself to have converged and will terminate. Type: float

**This class has many funcitons that are used for the incremental Page Rank calculation and other utilities.**

**Incremental Algorithm**
```
addgraph(graph)
```
This is the main function that implements the Incremental PageRank Algorithm. It separates the graph into two parts and implements PageRank only on the effected nodes, and simply scales the unaffected nodes.

Arguments:

1. **graph**: This is the graph containing the edges that are to be added into the graph.

**Normalized Page Ranks**
```
normalized_pagerank()
```
This function calculates the normalized page rank that can be used to compare two graphs based on this [paper](https://domino.mpi-inf.mpg.de/intranet/ag5/ag5publ.nsf/0/31deb7636690f704c125729c003181ef/$file/www2007.pdf).

**Plotting**
```
printgraph(node)
```
This function plots the history of the pagerank of the given node

**Average PageRank Calculation over time**
```
exppagerank(node,a)
```
This function calculates the average pagerank of the given node by exponential scaling.
Arguments:

1. **node**: This is the node for which the average is to be calculated.
2. **a**: This is the factor for exponential scaling

```
logpagerank(node,a)
```
This function calculates the average pagerank of the given node by logarithmic scaling.
Arguments:

1. **node**: This is the node for which the average is to be calculated.
2. **a**: This is the factor for logarithmic scaling

**PageRank Prediciton**
```
predict_pagerank1(node,x,i)
```
This function predicts the next pagerank value using polynomial fitting for the history of pageranks.
Arguments:

1. **node**: This is the node for which the page rank is to be predicted
2. **x**: This is the number of previous nodes to be used for prediciton
3. **i**: This is used to signify the timestamp of prediction. It is used to predict already calculated PageRanks, just for comparision. By default, it predicts the next node.

```
predict_pagerank2(node,x,i)
```
This function predicts the next pagerank value using polynomial fitting for the history of pagerank differentials.
Arguments:

1. **node**: This is the node for which the page rank is to be predicted
2. **x**: This is the number of previous nodes to be used for prediciton
3. **i**: This is used to signify the timestamp of prediction. It is used to predict already calculated PageRanks, just $

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

We need to install these libraries for proper functioning of the code

1.  [NetworkX](https://networkx.github.io/) used fo storing graphs
2.  [Matplotlib](http://matplotlib.org/) used for creating plots
3.  [Numpy](http://www.numpy.org/) used for interpolation of curves

### Installing

All the above librarie can be easily installed using apt-get in Ubuntu

```
sudo apt-get install python-networkx
sudo apt-get install python-numpy
sudo apt-get install python-matplotlib
```
## Running the tests

There are some tests that can be run, which calculates the PageRank for a given file with a list of edges using the incremental algorithm. It splits the file into 100 parts and calculates by adding each part at a time. It also prints the timeline of PageRank of 50 random nodes including actual, predicted and average values in a folder "figs".


```
python main.py filename
```
It can also be run in the interactive shell

```
import main
main.test(filename)
```

## Authors

* **Manne Naga Nithin** - [nithinmanne](https://github.com/nithinmanne)
* **Mekala Rajasekhar Reddy**

## Acknowledgments

* Group Project Partners
