# Tesla_Coding_Challenge
Implementing a priority expiry cache


My current implementation is using a mapping of cacheItems to heaps. 
The mapping consists of the key mapped two pointers that are doubly linked to two heaps (expiry and priority). 

The time complexity is O(log n) and space is O(N).

