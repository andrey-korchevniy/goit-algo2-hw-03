#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementation of the Edmonds-Karp maximum flow algorithm.
"""

from collections import deque
from typing import Dict, List, Tuple, Any

# Type aliases
NodeIndex = int
Flow = int
FlowMatrix = List[List[int]]
CapacityMatrix = List[List[int]]
Path = List[NodeIndex]


def bfs(capacity_matrix: CapacityMatrix, flow_matrix: FlowMatrix, 
        source: NodeIndex, sink: NodeIndex, parent: List[NodeIndex]) -> bool:
    """
    Performs breadth-first search to find an augmenting path in the residual network.
    
    Args:
        capacity_matrix: Matrix representing edge capacities
        flow_matrix: Matrix representing current flow
        source: Source node index
        sink: Sink node index
        parent: List to store path from source to sink
        
    Returns:
        bool: True if augmenting path exists, False otherwise
    """
    num_nodes = len(capacity_matrix)
    visited = [False] * num_nodes
    queue = deque([source])
    visited[source] = True
    
    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(num_nodes):
            residual_capacity = capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor]
            if not visited[neighbor] and residual_capacity > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False


def edmonds_karp(capacity_matrix: CapacityMatrix, source: NodeIndex, sink: NodeIndex) -> Tuple[Flow, FlowMatrix, List[Dict]]:
    """
    Implements Edmonds-Karp algorithm to find maximum flow in a network.
    
    Args:
        capacity_matrix: Matrix representing edge capacities
        source: Source node index
        sink: Sink node index
        
    Returns:
        Tuple containing:
        - Maximum flow value
        - Flow matrix showing flow on each edge
        - History of augmenting paths found
    """
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0
    path_history = []
    
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Find minimum residual capacity along the found path (bottleneck)
        path_flow = float('Inf')
        current_node = sink
        path = [sink]
        
        while current_node != source:
            previous_node = parent[current_node]
            residual_capacity = capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node]
            path_flow = min(path_flow, residual_capacity)
            current_node = previous_node
            path.append(current_node)
        
        path.reverse()  # Reverse to get path from source to sink
        
        # Update flow along the path, considering reverse flow
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Store path information for analysis
        path_history.append({
            'path': path,
            'flow': path_flow
        })
        
        # Increase maximum flow
        max_flow += path_flow
    
    return max_flow, flow_matrix, path_history 