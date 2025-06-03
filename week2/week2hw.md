1. ##### implement a hashtable that does the same thing as Python's built-in dictionary

   - *put*, *get*, *delete*, *size*, and hidden function *hash* (consider SHA-256 based hashing). 

   - try rehashing/resizing

     - try sizes with prime numbers (best) or odd numbers
     
   - resize up when data size > 70%, down when data size < 30%  - double/half the size and then find the closest prime number


> Questions: 
>
> when to resize: is it for a single bucket load, or for the overall table load when we consider resizing
>
> Since check_size() is required, I couldn’t reset item_count to 0 before re-inserting items (that would fail the size check). So to keep the correct count, I added item_count -= 1 after each put() in the loop. But this line does not look great—is there a cleaner way to handle this without breaking check_size()? 


2. ##### [non coding] why in reality tree structures sometimes are selected instead of hashtables while hashtables actually have smaller time complexity? 

   ​	thoughts: 

   - hash tables take up larger space - needs a size larger than data size to assign data entries with their hash value, trees only take up data sized space? 
   - trees allow easier categorizing since the left/right usually follow some sorting rules (thus representing some connections)? while data in hashtable do not really have relationships with their neighbors

   

3. ##### [non coding] Consider a data structure that stores cache data with a first-in-first-out rule forming a queue of <URL, Web page>. 

   - If an element is already in the queue and is revisited, it gets moved to the back of the queue

   - O(1) to **search** if a given pair is within cache or not most of the time, and **remove** the least recent pair, **add** given pair if not found, 

     > question: does **reorder** also have to be O(1)? 

   ###### 	Implementation thoughts: 

   consider linked list? to do the ordering, still utilizing hash table for O(1) lookup

   - pack elements in a class called *Node = (value, prev, next)*, 

   - hash table *table* stores Node, has property *head* and *end*. **search**: find element with hash value. 

     **remove**: to remove Node B, assign B.next to B.prev.next, and table[hash(B)] resets to none

     ​	case B.prev is none: B is head node, update table.head to 	B.next and reset B.next.prev to none. vice versa

     **add**: to add Node B, always adding to the back: 

     ​	table.end.next = B (if table.end is not none)

     ​	B.prev = table.end

     ​	table.end = B 

     **reorder**: within search when we found the target, we could do remove and then add. 

4. try implementing the cache structure in 3

challenge questions

1. is there a data structure that *always* does search-add-delete operations with O(1) complexity? 

   to ensure O(1), we need a way to search without iterations, so each item should have a key that helps us find it. 

