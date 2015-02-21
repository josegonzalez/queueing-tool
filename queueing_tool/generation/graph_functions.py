import graph_tool.all as gt
import numpy as np


def _test_graph(g) :
    """A function that makes sure ``g`` is either a :class:`~graph_tool.Graph` or 
     a string or file object to one.

    Parameters
    ----------
    g : A **str** or a :class:`~graph_tool.Graph`.

    Returns
    -------
    :class:`~graph_tool.Graph`
        If ``g`` is a string or a file object then the output given by
        ``graph_tool.load_graph(g, fmt='xml')``, if ``g`` is aready a 
        :class:`~graph_tool.Graph` then it is returned unaltered.

    Raises
    ------
    TypeError
        Raises a :exc:`~TypeError` if ``g`` is not a string to a file object,
        or a :class:`~graph_tool.Graph`\.
    """
    if isinstance(g, str) :
        g = gt.load_graph(g, fmt='xml')
    elif not isinstance(g, gt.Graph) :
        raise TypeError("Need to supply a graph-tool graph or the location of a graph")
    return g


def vertices2edge(g, u, v) :
    """Returns the edge index of the edge that connects two vertex.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
    u : int or :class:`~graph_tool.Vertex`
        The vertex index (or actual :class:`~graph_tool.Vertex`) identifying
        the source vertex.
    v : int or :class:`~graph_tool.Vertex`
        The vertex index (or actual :class:`~graph_tool.Vertex`) identifying
        the target vertex.

    Returns
    -------
    edge_index : int or ``None``
        If there is an edge connecting ``u`` and ``v`` then its edge index is
        returned, otherwise ``None`` is returned.
    """
    return g.edge_index[g.edge(u, v)]


def graph2dict(g) :
    """Takes a graph and returns an adjacency list.

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`

    Returns
    -------
    adj : :class:`.dict`
        A dictionary where a key is the vertex index for a vertex ``v`` and the
        values are :class:`.list`\s of vertex indices where that vertex is
        connected to ``v`` by an edge.
    eTypes : :class:`.dict` or ``None``
        A dictionary where a key is the vertex index for a vertex ``v`` and the
        values are :class:`.list`\s of each adjacent edge's edge type.
        More specifically, ``eType[v][k]`` is the edge type of the edge
        ``adj[v][k]``.
    """
    adj = {int(v) : [int(e.target()) for e in v.out_edges()] for v in g.vertices()}
    if 'eType' in g.ep :
        eTypes = {}
        for key, value in adj.items() :
            eTypes[key] = []
            for v in value :
                e = g.edge(key, v)
                eTypes[key].append( g.ep['eType'][e] )
    else :
        eTypes = None                
    return adj, eTypes


def shortest_paths_distances(g) :
    """Returns the shortest paths between every two vertices in the graph ``g``,
    as well as the total distances along those distances.

    Parameters
    ----------
    g : Graph
        A connected :class:`~graph_tool.Graph`.

    Returns
    -------
    shortest_path : :class:`~numpy.ndarray`
        A two-dimensional array where ``shortest_path[i,j]`` is the next vertex
        to visit if you want to take the shortest path from node ``i`` to node
        ``j``.
    distances : :class:`~numpy.ndarray`
        A two-dimensional array where ``distances[i,j]`` is the distance of the
        shortest path from node ``i`` to node ``j``.

    Raises
    ------
    TypeError
        Raises a :exc:`~TypeError` if ``g`` is not a string to a file object, or a 
        :class:`~graph_tool.Graph`.
    """
    g = _test_graph(g)

    v_props = set()
    for key in self.Qn.g.vertex_properties.keys() :
        v_props = v_props.union([key])

    nV    = g.num_vertices()
    dist  = zeros((nV, nV))
    short = np.ones( (nV, nV), int)
    spath = np.ones( (nV, nV), int)

    if 'dist' not in v_props :        
        dist  = zeros((nV, nV))

        for ve in g.vertices() :
            for we in g.vertices() :
                v,w  = int(ve), int(we)

                if v == w or dist[v, w] != 0 :
                    continue

                tmp   = gt.shortest_path(g, ve, we, weights=g.ep['edge_length'])
                path  = [int(v) for v in tmp[0]]
                elen  = [g.ep['edge_length'][e] for e in tmp[1]]

                for i in range(len(path) - 1):
                    for j in range(i+1, len(path)):
                        dist[path[i], path[j]] = sum(elen[i:j])

                spath[path[:-1], path[-1]] = path[1:]

                for j in range(1,len(path)-1) :
                    pa  = path[:-j]
                    spath[pa[:-1], pa[-1]] = pa[1:]

                if not g.is_directed() :
                    path.reverse()
                    spath[path[:-1], path[-1]] = path[1:]

                    for j in range(1, len(path)-1) :
                        pa  = path[:-j]
                        spath[pa[:-1], pa[-1]] = pa[1:]

            short[v, :] = spath[v, :]

        r = np.arange(nV)
        short[r, r] = r
    else :
        for v in g.vertices() :
            dist[int(v),:] = g.vp['dist'][v].a

    return short, dist
