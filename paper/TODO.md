TODO LIST FOR THE PAPER
====

# TOP PRIORITY

* Extend Lemma 2 to directed graphs.

* Experiments for Topk 



## Low Hanging

* Mention empirical VC-dimension (not sure about this?) 

* Discuss JACM variant (booringggg)



# LOW PRIORITY

* Choose journal

* Implement Bidirectional / A* search

* Check Kleinberg's dispersion. Can we do anything about it?



# UNDETERMINED PRIORITY

* Report analysis 1st reviewer WSDM to motivate top-k algo. I'm not sure about
this. Would look like we're shooting in our own foot.

* Compare the two algorithms in terms of how many updates they do. This
would highlight that BrandesPich do a great amount of unnecessary updates and that is
why they achieve better approximation that the user asked for.

* New definition of Betweenness for sets of nodes. This time the ranges
are the shortest paths that pass through at least one of the nodes. Paths that
pass through more nodes are still counted as one. Proof to me sounds like usual
lemma on unions/intersections or range spaces. Eli in his note does something
but IMHO is wrong (I don't get the last passage). Question is how to find those.
Eli suggests something, but IMHO is again wrong (the sum of nodes' betweennesses
only give an upper bound, which doesn't seem to help much, imho)

* Can we use s-t connectivity for BP? (I no longer know what that meant)

