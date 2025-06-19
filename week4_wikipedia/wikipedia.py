import sys
import collections
import math
import os
import pickle

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Extract 'small', 'medium', or 'large' from pages_file
        suffix = os.path.basename(pages_file).split("_")[-1].replace(".txt", "")
        # Name cache file by the size of input
        cache_file = f"cache_{suffix}.pkl"

        if os.path.exists(cache_file):
            print("Loading from cache...")
            with open(cache_file, "rb") as f:
                self.titles, self.links = pickle.load(f)

        else: 
            # Read the pages file into self.titles.
            with open(pages_file, encoding='utf-8') as file:
                for line in file:
                    (id, title) = line.rstrip().split(" ")
                    id = int(id)
                    assert not id in self.titles, id
                    self.titles[id] = title
                    self.links[id] = []
            print("Finished reading %s" % pages_file)

            # Read the links file into self.links.
            with open(links_file) as file:
                for line in file:
                    (src, dst) = line.rstrip().split(" ")
                    (src, dst) = (int(src), int(dst))
                    assert src in self.titles, src
                    assert dst in self.titles, dst
                    self.links[src].append(dst)
            print("Finished reading %s" % links_file)
            print()
            with open(cache_file, "wb") as f:
                pickle.dump((self.titles, self.links), f)
            print("Cache saved as {cache_file}!")


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the link to given title. Helper method
    def find_link(self, title): 
        for page_id, page_title in self.titles.items(): 
            if page_title == title: 
                return page_id
        return -1


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        link_queue = collections.deque()
        visited = set()

        start_link = self.find_link(start)
        goal_link = self.find_link(goal)
        if start_link == -1 or goal_link == -1: 
            return []

        parent_links = {start_link: None}
        visited.add(start_link)
        link_queue.append(start_link)

        while len(link_queue) > 0: 
            curr_link = link_queue.popleft()
            if curr_link == goal_link: 
                path = []
                while curr_link is not None: 
                    path.append(self.titles[curr_link])
                    curr_link = parent_links[curr_link]
                path.reverse()
                print("Found shortest path " + str(path))
                return path
            
            for child_link in self.links[curr_link]:
                if child_link not in visited:
                    visited.add(child_link)
                    parent_links[child_link] = curr_link
                    link_queue.append(child_link)

        print("No path is found!")
        return []


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pageranks = {}
        damping_factor = 0.85
        page_count = len(self.titles)

        # 1. Initialize pageranks to 1.0 for each page
        for page_id in self.titles.keys():
            pageranks[page_id] = 1.0

        while True:
            new_ranks = {page_id: 0.0 for page_id in self.titles.keys()}
            share_for_all = 0.0
            # 2. Distribute 85% of rank to children, the rest 15% to all
            #    If no children, distribute 100% evenly to all pages
            for page_id, rank in pageranks.items(): 
                children = self.links[page_id]
                if len(children) > 0: 
                    share_for_child = damping_factor * rank / len(children)
                    share_for_all += (1 - damping_factor) * rank / page_count
                    for child in children: 
                        new_ranks[child] += share_for_child
                else: 
                    share_for_all += rank / page_count
            for page_id in self.titles.keys(): 
                new_ranks[page_id] += share_for_all

            # 3. Make sure the sum of page ranks is always constant
            print(sum(new_ranks.values()), sum(pageranks.values()))
            assert(math.isclose(sum(new_ranks.values()), sum(pageranks.values())))

            # 4. End distribution when difference is negligible
            diff = sum((new_ranks[page_id] - pageranks[page_id])**2 for page_id in self.titles)
            pageranks = new_ranks
            if diff < 0.01: 
                break
    
        # 5. Sort pages based on page rank and print top 10
        sorted_pages = sorted(pageranks.items(), key = lambda x: x[1], reverse=True)
        print("\nTop 10 popular pages: ")
        for page_id, rank in sorted_pages[:10]: 
            print(f"{self.titles[page_id]}: {rank:.5f}")


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    #wikipedia.find_longest_titles()
    #wikipedia.find_most_linked_pages()
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
