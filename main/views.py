from ntpath import join
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
#from .forms import NameForm
from typing import Any
from queue import PriorityQueue
from .models import graph,heuristic
from django.template import loader
from django.urls import reverse

def index(request):
    '''objects = graph.objects.all()
    res ='Printing all Dreamreal entries in the DB : <br>'

    for elt in objects:
      res += elt.city_name1+"<br>"'''
    #mygraph= graph.objects.all()
    myheuristic=heuristic.objects.all()
    return render(request, 'index.html',{'myheuristic': myheuristic})

def edit(request):

    mygraph= graph.objects.all().values()

    template = loader.get_template('edit.html')
    context = {
        'mygraph': mygraph,

    }
    return HttpResponse(template.render(context, request))

def edits(request):

    myheuristic = heuristic.objects.all().values()
    template = loader.get_template('edits.html')
    context = {

        'myheuristic': myheuristic,
    }
    return HttpResponse(template.render(context, request))

def add1(request):
    template = loader.get_template('add1.html')
    return HttpResponse(template.render({}, request))

def add2(request):
    template = loader.get_template('add2.html')
    return HttpResponse(template.render({}, request))

def addform1(request):
    b = request.POST['city_name1']
    c = request.POST['city_name2']
    d = request.POST['actual_distance']
    Graph = graph(city_name1=b, city_name2=c,actual_distance=d)
    Graph.save()
    return HttpResponseRedirect(reverse('edit'))
    #return HttpResponseRedirect(reverse('edit'))
def addform2(request):
    #def_addheuristic(request):
    e = request.POST['heuristic_name']
    f = request.POST['heuristic_value']
    Heuristic = heuristic(heuristic_name=e, heuristic_value=f)
    Heuristic.save()
    return HttpResponseRedirect(reverse('edits'))

def delete1(request, id):
    Graph = graph.objects.get(id=id)
    Graph.delete()
    return HttpResponseRedirect(reverse('edit'))

def delete2(request, id):
    Heuristic = heuristic.objects.get(id=id)
    Heuristic.delete()
    return HttpResponseRedirect(reverse('edits'))

def update(request, id):

    mygraph= graph.objects.get(id=id)

    template = loader.get_template('update.html')
    context = {

        'mygraph': mygraph,

    }
    return HttpResponse(template.render(context, request))

def update2(request, id):


    myheuristic = heuristic.objects.get(id=id)
    template = loader.get_template('update2.html')
    context = {


        'myheuristic': myheuristic,
    }
    return HttpResponse(template.render(context, request))

def updaterecord (request, id):
    b = request.POST['city_name1']
    c = request.POST['city_name2']
    d = request.POST['actual_distance']
    mygraph= graph.objects.get(id=id)
    mygraph.city_name1=b
    mygraph.city_name2=c
    mygraph.actual_distance=d
    mygraph.save()
    return HttpResponseRedirect(reverse('edit'))

def updaterecord2(request, id):
    e = request.POST['heuristic_name']
    f = request.POST['heuristic_value']
    myheuristic = heuristic.objects.get(id=id)
    myheuristic.heuristic_name=e
    myheuristic.heuristic_value=f
    myheuristic.save()
    return HttpResponseRedirect(reverse('edits'))

class Graph2:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.name, self.f))
# A* search
def astar_search(graph, heuristics, start, end):

    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)

    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            return path[::-1]
        # Get neighbours
        neighbors = graph.get(current_node.name)
        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            # Calculate full path cost
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None
# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True
# The main entry point for this module

def processed(request):

    graph2 = Graph2()
    # Create graph connections (Actual distance)
    graph3= graph.objects.all()

    for i in graph3:
        graph2.connect(i.city_name1, i.city_name2, i.actual_distance)
        graph2.make_undirected()


    # Create heuristics (straight-line distance, air-travel distance)

    heuristics2 = heuristic.objects.all()
    # Create graph connections (Actual distance)

    heuristics = {}
    for j in heuristics2:

        heuristics[j.heuristic_name]=j.heuristic_value


    if request.method == 'POST':


        Source = request.POST["Source"]
        Goal = request.POST["Goal"]
        path = astar_search(graph2, heuristics, Source, Goal)


        '''
        heuristics = {}

        heuristics['Basel'] = 204
        heuristics['Bern'] = 247
        heuristics['Frankfurt'] = 215
        heuristics['Karlsruhe'] = 137
        heuristics['Linz'] = 318
        heuristics['Mannheim'] = 164
        heuristics['Munchen'] = 120
        heuristics['Memmingen'] = 47
        heuristics['Nurnberg'] = 132
        heuristics['Passau'] = 257
        heuristics['Rosenheim'] = 168
        heuristics['Stuttgart'] = 75
        heuristics['Salzburg'] = 236
        heuristics['Wurzburg'] = 153
        heuristics['Zurich'] = 157
        heuristics['Ulm'] = 0'''


    else:
        return HttpResponseRedirect('/')
    return render(request, 'processed.html', {'path': path})
    #return render(request,'processed.html',{'heuristic':heuristic},{'cost':cost})



