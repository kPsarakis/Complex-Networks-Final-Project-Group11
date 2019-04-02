# Complex-Networks-Final-Project

## Summary
This project attempts to model the behaviour of customers' co-purchasing decisions on the amazon product review dataset. The goal is to predict the distribution, and potentially even the graph popularity (By some graph measure)

We approximate the number of purchases (as a measure of relative popularity) by the number of reviews on a given product. This serves as our true distribution. We then have a series of experiments of different models to predict the popularity from the graph topology:
	1. Random walk: 
	2. Generalized random walk: at timestep t, incorporates the number of times we've already visited our neighbours into our probability to visit that node
	3. Best method (1 or 2, to be decided) with removal: Removing popular nodes, how resilient is our predictive model to changes in the network.

## Data directories
- Raw data comes from the stanford SNAP dataset (http://snap.stanford.edu/data/com-Amazon.html), and is ommited due to size
- ```data/Interim``` directory contains intermediate results from transforming the dataset
- ```data/processed``` directory contains transformed data as edges, and popularity measures (as a baseline true distribution). Also contains pickle '.p' files that are cached versions of our graph (for efficiency, can be reconstructed from code)
- ```data/results``` Contains the raw results from running the algorithm on the different datasets (full graph, largest connected subset, random sample of size) for our different predictive models/

