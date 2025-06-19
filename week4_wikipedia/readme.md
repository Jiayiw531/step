
# Graph Algorithms

1. find_shortest_path(start, goal)
- Uses Breadth-First Search (BFS) to return the shortest path between two pages.
- Cycle-safe and guarantees the shortest path in unweighted graphs.
- Caching is implemented to speed up repeated queries on the same file.

2. find_most_popular_pages()
- Computes PageRank values iteratively.
- Returns the top 10 most popular pages based on converged ranks.
- Avoids full sort using a more efficient O(n) selection method.

output for small: 
> Loading from cache...kipedia.py' 'wikipedia_dataset/pages_small.txt' 'wikipedia_dataset/links_sFrom 渋谷 to パレートの法則, shortest path found['渋谷', 'C', 'パレートの法則']
From パレートの法則 to 渋谷, shortest path found['パレートの法則', 'C', '渋谷']
From C to E, shortest path found['C', 'E']
From A to A, shortest path found['A']
From 孤立ノード to 孤立ノード, shortest path found['孤立ノード']
From 渋谷 to 孤立ノード, no path is found!
Top 10 popular pages:
E: 1.44793
C: 1.42410
D: 1.31766
パレートの法則: 1.23445
ループノード: 1.11888
渋谷: 0.82786
A: 0.46129
孤立ノード: 0.16783

output for medium: 
> Loading from cache...
From 渋谷 to パレートの法則, shortest path found['渋谷', 'マクドナルド', 'Twitter', 'パレートの法則']
From パレートの法則 to 渋谷, shortest path found['パレートの法則', 'イタリア', 'クリスマス', '渋谷']
From C to E, shortest path found['C', 'E']
From A to A, shortest path found['A']
Top 10 popular pages:
英語: 1507.29770
ISBN: 959.70713
2006年: 526.10136
2005年: 502.26093
2007年: 491.48185
東京都: 480.27395
昭和: 459.37581
2004年: 445.36975
2003年: 404.73836
2000年: 401.88955



3. implement DFS with stack so that it traverses in the order of DFS with recursion



### notes from mentor: 

#### Testing Strategy
Tests are designed to include:
- Basic functionality
  - E.g., connected small graph, single known path.
- Edge cases
  - Empty graph, same start and goal node, self-loops.
- Special cases
  - Cycles in the graph
  - Multiple shortest paths
  - Goal not reachable

#### Design notes & revisions
1. Shortest Path:
    - Visited structure: simplified to a set instead of a dictionary.
    - Time Complexity: 
    - O(N + E) due to each node and edge being visited at most once.

2.  PageRank:
    - Top-10 optimization:  
    - Instead of <sorted(ranks.items(), key=...)>, we could use an O(N) selection algorithm 
    - Termination condition:  
    - Converges when the sum of squared differences between iterations is small enough.  
    - Test cases include inputs where:
        - Convergence happens quickly (e.g., uniform graphs)
        - Pages with no outgoing links are handled correctly
    - Improvement: `share_for_all` is now added only once per iteration instead of during every nested loop pass.


#### Time complexity analyses 
could be different from simply reading the upper bound of loop iterations. 
Say, for BFS, since we are sure to not visit any node twice, even if code says <for child_link in self.links[curr_link]:>, we could say that time complexity is essentially O(E) since it is followed by <if child_link not in visited:>, ensuring each edge / child to be visited at most once. This keeps the traversal efficient.
