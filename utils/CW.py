import numpy as np
import networkx as nx
from tqdm import tqdm

def get_similarity(embeddings,current_face_emb):
    """Returns an array containing the cosine similarity between a given face's embedding and an
    of other face embeddings 

    Args:
        embeddings : numpy array consisting of the embeddings
        current_face_emb : numpy array consisiting of embedding for a single face
    Returns:
        a numpy array containing cosine similarities between embeddings and current_face_emb
    """
    # current_face is broadcasted to 0th axis of embeddings
    # NOTE: Cosine similarity between two vectors a and b is (a.b)/(||a||*||b||). But for the embeddings we already normalized them such that ||a|| and ||b|| are 1.
    return np.sum(embeddings*current_face_emb,axis=1)

def draw_graph(data,threshold):
    """Draws a networkx graph in which each node represents an image in the corpus.
    The attributes of the node contain the embedding of the image computed by the face descriptor
    and the cluster it belongs to. Initially all the images are given their own cluster

    Args:
        data : The list of dictionaries containing the embeddings. (obtained by running the script `embedder.py` and loading the pickle file generated)
        threshold(阈值) : Minimum cosine similarity required between two face embeddings to form an edge between their respective nodes.

    Returns:
        G: the initial networkx graph required for the Chinese Whispers algorithm
    """
    G = nx.Graph()
    # Lists used to store nodes and edges for a graph
    G_nodes = []
    G_edges = []

    # Create a numpy array containing all the embeddings
    embeddings = np.array([dictionary['embedding'] for dictionary in data])

    # Iterate through  all embeddings computed from the corpus
    for index, embedding in enumerate(tqdm(data,desc="Creating graph")):

        # current_node represents the unique number by which a node is identified
        # Each face in the corpus is assigned to a node which contains the cluster of the node and the path to the image containing the face as attributes.
        # Initially all the faces are assigned to a their own cluster.
        # If an image contains two or more faces the respective number of nodes corresponding to each face is initialized.
        # After a specific number of iterations the algorithm groups similar faces into the same cluster.

        current_node = index+1
        
        node = (current_node, {'cluster':"Person {}".format(current_node),"source":data[index]["path"]})
        G_nodes.append(node)

        if current_node >= len(data):
            break
        # Get the cosine similarities for the face embedding of the current node and all the subsequent face embeddings
        # We only need to calculate for the subsequent ones because we already calculated for previous ones in earlier iterations and the edges have already been formed by the code below
        similarities = get_similarity(embeddings[index+1:],data[index]["embedding"])

        # list all the edges for current node
        current_node_edges = []

        # iterate through the similarities  
        for i,weight in enumerate(similarities):
            
            # Add an edge between the current face embedding's node and the other face embedding's node
            # if the cosine similarity is greater than the threshold
            if weight > threshold:
                # we add a weighted edge where the weight is the cosine similarity.
                current_node_edges.append((current_node,current_node+i+1,{"weight":weight}))

        # concatenate the current edges to the list
        G_edges = G_edges + current_node_edges
   
    G.add_nodes_from(G_nodes)
    G.add_edges_from(G_edges)

    return G

def chinese_whispers(G,iterations):
    """Applies the Chinese Whispers algorithm to the graph

    Args:
        G : networkx graph to represent the face embeddings
        iterations : number of iterations for the algorithm

    Returns:
        G: networkx graph where the embeddings are clustered
    """

    for _ in tqdm(range(iterations),desc="Iterations"):
        # Get all the nodes of the graph and shuffle them
        nodes = np.array(G.nodes())
        np.random.shuffle(nodes)

        # Iterate through the shuffled nodes
        for node in nodes:
            # Get the neighbours for the node
            neighbours = G[node]

            neighbour_clusters = {}
            #Firstly collect all the clusters the neighbours belong to. (does not iterate if no neighbours are present)
            for neighbour in neighbours:
                # For a given neighbour check the cluster it belong to.
                # For the same key in the dictionary add the weight between the node and the current neighbour to the value of the key 
                # (i.e we are calculating the sum of weights of edges in the neighbours which belong to a particular cluster)

                if G.nodes[neighbour]['cluster'] in neighbour_clusters:
                    
                    neighbour_clusters[G.nodes[neighbour]['cluster']] += G[node][neighbour]['weight']
                else:
                    neighbour_clusters[G.nodes[neighbour]['cluster']] = G[node][neighbour]['weight']
                
            weight_sum = 0
            best_cluster = None

            # The best cluster for the particular node is then the
            # cluster whose sum of edge weights to the node is maximum for the edges the node belongs to. 
            for cluster in neighbour_clusters:
                if neighbour_clusters[cluster] >  weight_sum:
                    weight_sum = neighbour_clusters[cluster]
                    best_cluster = cluster

            # If the embedding is not close to any other embedding (i.e only one picture of the person) dont change the cluster
            if best_cluster is None:
                continue

            G.nodes[node]['cluster'] = best_cluster

    return G
