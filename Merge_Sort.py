import graphviz
import numpy as np
import time
from IPython.display import clear_output, display

# Used to count nodes and name them like node 1, node 2, ...
node_counter = 0

def display_graph(digraph, delay):
    # self explanatory, refresh and remove previous output
    clear_output(wait=True)
    # print the graph
    display(digraph)
    # moments before printing another and removing previous graph
    time.sleep(delay)

def merge(arr, left, mid, right, digraph, left_node, right_node):
    # to make the value change as we will keep increasing the counter
    global node_counter

    # node name, will be used to be put in .node as a parameter and used later to add edges 
    merge_node = f'node_{node_counter}'
    node_counter += 1

    # showcase the words to be typed in the node, in this case it could be something like
    # Merge
    # [3] & [1]
    merge_label = f"Merge\n{arr[left:mid+1]} & {arr[mid+1:right+1]}"

    # add a node named node_(node num), as a box shape, filled with yellow color
    digraph.node(merge_node, label=merge_label, shape="box", style="filled", fillcolor="yellow")

    # The graph could be something like this
    # Split [3]      Split [1]
    #       Merge [3] & [1]
    # And we want the split 3 and split 1 be linked to merge 3 & 1
    # specifically split 3 TO merge and split 1 TO merge
    digraph.edge(left_node, merge_node)
    digraph.edge(right_node, merge_node)

    # display graph
    display_graph(digraph, delay=0.5)

    
    # Merging process that you probably can find in geekofgeeks
    # to be fair the concept is similar because you know, it is an algorithm
    n1 = mid - left + 1
    n2 = right - mid
    L = arr[left:left + n1]
    R = arr[mid + 1:mid + 1 + n2]
    
    i = j = 0
    k = left
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
        
    # node name, will be used to be put in .node as a parameter and used later to add edges, the end is near
    merge_result_node = f'node_{node_counter}'
    node_counter += 1

    # showcase the words to be typed in the node
    result_label = f"Sorted\n{arr[left:right+1]}"

    # add a node named node_(node num), as a box shape, filled with light green color because green means correctly tho it is mostly subjective
    digraph.node(merge_result_node, label=result_label, shape="box", style="filled", fillcolor="lightgreen")
    
    # connect merge node i.e. sth like Merge [3] & [1] to this merge result or sorted node
    
    digraph.edge(merge_node, merge_result_node)
    display_graph(digraph, delay=0.5)
    return merge_result_node

def merge_sort(arr, left, right, digraph, parent_node=None):

    # to make the value change as we will keep increasing the counter
    global node_counter

    # node name, will be used to be put in .node as a parameter and used later to add edges 
    current_node = f'node_{node_counter}'
    node_counter += 1

    # showcase the words to be typed in the node
    current_label = f"Split\n{arr[left:right+1]}"

    # add a node named node_(node num), as a box shape, filled with pink color,
    # with the content of the array's content
    digraph.node(current_node, label=current_label, shape="box", style="filled", fillcolor="pink")

    # if it has a parent node then we should link the parent node to current node to make it looks connected
    if parent_node is not None:
        digraph.edge(parent_node, current_node)

    # display the graph for 0.5 sec before changing
    display_graph(digraph, delay=0.5)


    # Remember that the array may look like this [3, 1, 4, 2]
    # then originally left will be 0 and right will be 4-1 = 3
    # when left >= right that means right is either 0 or below for left case
    # the mid below will help with the recursion by changing that right to the mid
    # [3,1,4,2] -> mid = (0+3)//2 = 1 = new right -> [3,1] -> mid = (0+1) // 2 = 0 = new right
    # Then we will return the current node as it is already "sorted" (one element in array so it is technically sorted)
    if left >= right:
        return current_node
    mid = (left + right) // 2
    left_node = merge_sort(arr, left, mid, digraph, current_node)
    
    # same procedure but for right array
    right_node = merge_sort(arr, mid+1, right, digraph, current_node)

    # After sorting the partial left and right array we will have to merge them
    merge_result_node = merge(arr, left, mid, right, digraph, left_node, right_node)
    
    # Connect merge result back to the current splited node, dashed style --- because I want it to connect but not directly connect
    digraph.edge(current_node, merge_result_node, style="dashed")
    return merge_result_node



# ---------MAIN-------------------

# Testing array, just comment 3142 and uncomment that random if you wish to
# arr = [3, 1, 4, 2]
arr = np.random.randint(1, 20, size=8).tolist()
print(f"Initial Array: {arr}")

dot = graphviz.Digraph(comment="Merge Sort Tree")

# This will make the tree goes from top to bottom
# You can go with LR but I prefer TB cuz more tree looking
dot.attr(rankdir='TB')

# Root node name will be node_0, which is the unsorted array
# This will be the starting point and node counter will be incremented for future nodes "name"
root_node = f'node_{node_counter}'
node_counter += 1

# Initialize the first node, which is root node aka node_0 as starting point
# the code itself is quite self explanatory
# box shape node, orange colored and filled
dot.node(root_node, label=f"Original Array:\n{arr}", shape="box", style="filled", fillcolor="orange")

#Print the graph first graph, the delay can be changed to change the output speed to 1 image per delay seconds
delay = 1 # seconds
# We can do something like display_graph(dot, delay=1) but i have done it like that for the sake of demonstration
display_graph(dot, delay)

final_node = merge_sort(arr, 0, len(arr)-1, dot, root_node)

# Connect the final merge result to the root node
dot.edge(final_node, root_node, style="dashed")

# save the last form to a file
dot.render('merge_sort_tree', format='png', cleanup=True)

# notify us the program is finished
print("Final Sorted Array:", arr)
