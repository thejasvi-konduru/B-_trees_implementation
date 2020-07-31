For B+ trees with multiple occurrences of the same number
1.The insertion algorithm remains the same.
2.The FIND,COUNT,RANGE algorithm changes i.e if the given query key is equal to a ith key in the node then we have to check from the ith child subtree instead of checking from (i+1)st child subtree because due to multiple occurrences the query key can be present in the ith child's subtree also.
3.The above changes in the algorithm gives us the correct answer even for multiple occurrences of the same item in B+ trees.