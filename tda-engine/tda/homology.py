import numpy as np
import scipy.spatial.distance as dist
from .union_find import UnionFind

class PersistentHomology:
    def __init__(self, points):
        self.points = np.array(points)
        self.n_points = len(points)
        self.dist_matrix = dist.squareform(dist.pdist(self.points))

    def compute_h0_persistence(self):
        edges = []
        for i in range(self.n_points):
            for j in range(i + 1, self.n_points):
                edges.append((self.dist_matrix[i, j], i, j))
        edges.sort(key=lambda x: x[0])

        uf = UnionFind(self.n_points)
        birth_times = {i: 0.0 for i in range(self.n_points)}
        persistence_h0 = []

        for d, u, v in edges:
            united, root1, root2 = uf.union(u, v)
            if united:
                younger_root = root2 if uf.find(root1) == root1 else root1
                older_root = root1 if younger_root == root2 else root2
                death = d
                birth = birth_times[younger_root]
                if death > birth:
                    persistence_h0.append((birth, death))

        final_components = set(uf.find(i) for i in range(self.n_points))
        for c in final_components:
            persistence_h0.append((birth_times[c], np.inf))

        return persistence_h0

    def compute_h1_persistence(self, max_edge_len):
        edges = []
        for i in range(self.n_points):
            for j in range(i + 1, self.n_points):
                if self.dist_matrix[i, j] <= max_edge_len:
                    edges.append((self.dist_matrix[i, j], i, j))
        edges.sort(key=lambda x: x[0])

        adj = {i: set() for i in range(self.n_points)}
        triangles = []

        for d, u, v in edges:
            common = adj[u].intersection(adj[v])
            for w in common:
                d_uw = self.dist_matrix[u, w]
                d_vw = self.dist_matrix[v, w]
                max_d = max(d, d_uw, d_vw)
                triangles.append((max_d, tuple(sorted([u, v, w]))))
            adj[u].add(v)
            adj[v].add(u)

        triangles.sort(key=lambda x: x[0])

        cycles = {}
        persistence_h1 = []

        for d, u, v in edges:
            path = self._find_shortest_path(u, v, adj, exclude=(u, v))
            if path:
                cycle_edges = tuple(sorted([(path[k], path[k+1]) for k in range(len(path)-1)] + [(min(u, v), max(u, v))]))
                cycles[cycle_edges] = d

        for d_tri, tri in triangles:
            u, v, w = tri
            tri_edges = {
                (min(u, v), max(u, v)),
                (min(u, w), max(u, w)),
                (min(v, w), max(v, w))
            }
            to_remove = []
            for cycle_edges, birth in cycles.items():
                if tri_edges.issubset(set(cycle_edges)):
                    if d_tri > birth:
                        persistence_h1.append((birth, d_tri))
                    to_remove.append(cycle_edges)
            for c in to_remove:
                del cycles[c]

        for birth in cycles.values():
            persistence_h1.append((birth, max_edge_len * 1.2))

        return persistence_h1

    def _find_shortest_path(self, start, end, adj, exclude):
        queue = [[start]]
        visited = {start}
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                return path
            for neighbor in adj[node]:
                edge = (min(node, neighbor), max(node, neighbor))
                if edge == exclude:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None
