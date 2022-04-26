MAX_NAME_LEN = 4

class NameLenError(Exception): pass

class Node:
    def __init__(self, name):
        self.name = name
        if len(name) > MAX_NAME_LEN:
            print("Name", name, "exceeds max name len")
            raise NameLenException
        self.children = [None, None]

all_nodes = []

def add_node(name, children = None):
    global all_nodes
    all_nodes.append(Node(name))
    if children is not None:
        all_nodes[-1].children = children
        
        
add_node("5")
add_node("31")
add_node("48")
add_node("60", [12, 11])
add_node("92", [13, None])
add_node("20", [0, 1])
add_node("45", [5, 2])
add_node("88", [None, 4])
add_node("98", [7, None])
add_node("76", [3, 8])
add_node("50", [6, 9])
add_node("128")
add_node("134")
add_node("312")


# [line_no, above=True, node]
current_layer = [[0, True, all_nodes[10]]]
# Current output
lines = [""]
# [from, to, pos] - Keeps branches linked together
links = []

new_line = ""
while len(current_layer) > 0:
    offset = 0
    new_layer = []
    line_no = -1
    for node in current_layer:
        if node[0] == line_no:
            lines[line_no+offset] = lines[line_no+offset][:-1] + "┤"
        else:
            line_no = node[0]
            if node[1]:
                lines[line_no+offset] += "┘"
            else:
                lines[line_no+offset] += "┐"
                
        sub_offset = 0
        if not node[1]: sub_offset += 1
        
        name = ("-"*(MAX_NAME_LEN - len(node[2].name))) + node[2].name
        if node[1]:
            branch_char = "┌"
        else:
            branch_char = "└"
        
        to_insert = new_line+branch_char+name
        pos = node[0]+offset+sub_offset
        addition = 0
        
        # Insert Links
        for i in links:
            if i[0] < node[0]+offset+sub_offset <= i[1]:
                if len(to_insert)-1 >= i[2]:
                    to_insert = to_insert[:i[2]] + "|" + to_insert[i[2]+1:]
                else:
                    to_insert = to_insert[:i[2]] + "|"
                addition += 1
        
        lines.insert(pos, to_insert)
        
        index = len(new_line)
        
        if node[2].children[0] is not None:
            new_layer.append([node[0]+offset+sub_offset, True, all_nodes[node[2].children[0]]])
        if node[2].children[1] is not None:
            new_layer.append([node[0]+offset+sub_offset, False, all_nodes[node[2].children[1]]])
    
        
        offset += 1
        
        # Update links for new line
        for i in links:
            if i[0] >= pos:
                i[0] += 1
            if i[1] >= pos:
                i[1] += 1
        
        links.append([node[0]+offset-1, node[0]+offset, index])
        
    new_line += " "*MAX_NAME_LEN + " "
    current_layer = new_layer
    
for i in lines:
    print(i)
