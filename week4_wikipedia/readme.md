
# Graph Algorithms

1. find_shortest_path(start, goal)
- Uses Breadth-First Search (BFS) to return the shortest path between two pages.
- Cycle-safe and guarantees the shortest path in unweighted graphs.
- Caching is implemented to speed up repeated queries on the same file.

2. find_most_popular_pages()
- Computes PageRank values iteratively.
- Returns the top 10 most popular pages based on converged ranks.
- Avoids full sort using a more efficient O(n) selection method.

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
