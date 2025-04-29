#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logistics network construction and analysis.
"""

from typing import Dict, List, Tuple, Any

# Type aliases
Node = str
NodeIndex = int
Flow = int
Capacity = int
FlowMatrix = List[List[int]]
CapacityMatrix = List[List[int]]


def build_logistics_network() -> Tuple[List[Node], Dict[Node, NodeIndex], CapacityMatrix]:
    """
    Builds the logistics network with terminals, warehouses, and stores.
    
    Returns:
        Tuple containing:
        - List of all nodes in the network
        - Mapping of node names to indices
        - Capacity matrix representing edge capacities
    """
    # Define node types
    terminals = ["Термінал 1", "Термінал 2"]
    warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
    stores = [f"Магазин {i}" for i in range(1, 15)]
    
    # Create a mapping of node names to indices
    nodes = terminals + warehouses + stores
    node_indices = {node: i for i, node in enumerate(nodes)}
    
    # Initialize capacity matrix with zeros
    n = len(nodes)
    capacity_matrix = [[0] * n for _ in range(n)]
    
    # Define edges with capacities from the given data
    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    
    # Fill capacity matrix
    for from_node, to_node, capacity in edges:
        from_idx = node_indices[from_node]
        to_idx = node_indices[to_node]
        capacity_matrix[from_idx][to_idx] = capacity
    
    return nodes, node_indices, capacity_matrix


def calculate_terminal_to_store_flow(flow_matrix: FlowMatrix, node_indices: Dict[Node, NodeIndex]) -> List[Tuple[Node, Node, Flow]]:
    """
    Calculates the flow between terminals and stores through warehouses.
    
    Args:
        flow_matrix: Matrix representing current flow
        node_indices: Mapping of node names to indices
        
    Returns:
        List of tuples containing (terminal, store, flow_amount)
    """
    results = []
    terminals = ["Термінал 1", "Термінал 2"]
    stores = [f"Магазин {i}" for i in range(1, 15)]
    warehouses = ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]
    
    # Create a dict to track flow from each terminal to each store
    terminal_store_flows = {(t, s): 0 for t in terminals for s in stores}
    
    # Calculate incoming flow to each warehouse from each terminal
    warehouse_inflows = {}
    for w in warehouses:
        w_idx = node_indices[w]
        warehouse_inflows[w] = {}
        
        for t in terminals:
            t_idx = node_indices[t]
            if flow_matrix[t_idx][w_idx] > 0:
                warehouse_inflows[w][t] = flow_matrix[t_idx][w_idx]
    
    # Calculate outgoing flow from each warehouse to each store
    for w in warehouses:
        w_idx = node_indices[w]
        total_outflow = sum(flow_matrix[w_idx][node_indices[s]] for s in stores)
        
        if total_outflow > 0:
            for s in stores:
                s_idx = node_indices[s]
                store_flow = flow_matrix[w_idx][s_idx]
                
                if store_flow > 0:
                    # Distribute the flow proportionally from each terminal
                    for t, terminal_flow in warehouse_inflows[w].items():
                        # Calculate proportion of flow from this terminal through this warehouse
                        proportion = store_flow / total_outflow
                        # Calculate estimated flow from terminal to store
                        t_to_s_flow = round(proportion * terminal_flow)
                        
                        if t_to_s_flow > 0:
                            terminal_store_flows[(t, s)] += t_to_s_flow
    
    # Convert results to a list format
    return [(terminal, store, flow) for (terminal, store), flow in terminal_store_flows.items() if flow > 0]


def analyze_network(capacity_matrix: CapacityMatrix, flow_matrix: FlowMatrix, 
                   nodes: List[Node], node_indices: Dict[Node, NodeIndex], 
                   path_history: List[Dict]) -> Dict[str, Any]:
    """
    Analyzes the network to identify bottlenecks and improvement opportunities.
    
    Args:
        capacity_matrix: Matrix representing edge capacities
        flow_matrix: Matrix representing current flow
        nodes: List of all nodes in the network
        node_indices: Mapping of node names to indices
        path_history: History of augmenting paths
        
    Returns:
        Dictionary containing analysis results
    """
    analysis = {}
    
    # Find bottlenecks (edges where flow = capacity)
    bottlenecks = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if capacity_matrix[i][j] > 0 and flow_matrix[i][j] == capacity_matrix[i][j]:
                bottlenecks.append((nodes[i], nodes[j], capacity_matrix[i][j]))
    
    analysis["bottlenecks"] = bottlenecks
    
    # Find terminals with highest outflow
    terminal_outflows = {}
    for t in ["Термінал 1", "Термінал 2"]:
        t_idx = node_indices[t]
        outflow = sum(flow_matrix[t_idx])
        terminal_outflows[t] = outflow
    
    analysis["terminal_outflows"] = terminal_outflows
    
    # Find stores with lowest inflow
    store_inflows = {}
    for s in [f"Магазин {i}" for i in range(1, 15)]:
        s_idx = node_indices[s]
        inflow = sum(flow_matrix[i][s_idx] for i in range(len(nodes)))
        store_inflows[s] = inflow
    
    # Sort stores by inflow
    analysis["store_inflows"] = {k: v for k, v in sorted(store_inflows.items(), key=lambda item: item[1])}
    
    # Find warehouse utilization
    warehouse_utilization = {}
    for w in ["Склад 1", "Склад 2", "Склад 3", "Склад 4"]:
        w_idx = node_indices[w]
        
        # Calculate incoming flow for warehouse
        inflow = sum(flow_matrix[i][w_idx] for i in range(len(nodes)) if i != w_idx)
        
        # Calculate outgoing flow from warehouse
        outflow = sum(flow_matrix[w_idx][j] for j in range(len(nodes)) if j != w_idx)
        
        # Calculate total capacity in and out
        total_in_capacity = sum(capacity_matrix[i][w_idx] for i in range(len(nodes)) if i != w_idx)
        total_out_capacity = sum(capacity_matrix[w_idx][j] for j in range(len(nodes)) if j != w_idx)
        
        warehouse_utilization[w] = {
            "inflow": inflow,
            "outflow": outflow,
            "in_capacity": total_in_capacity,
            "out_capacity": total_out_capacity,
            "in_utilization": round(inflow / total_in_capacity * 100) if total_in_capacity > 0 else 0,
            "out_utilization": round(outflow / total_out_capacity * 100) if total_out_capacity > 0 else 0
        }
    
    analysis["warehouse_utilization"] = warehouse_utilization
    
    # Analyze path history
    analysis["paths"] = path_history
    
    return analysis


def get_edges_from_matrix(capacity_matrix: CapacityMatrix, nodes: List[Node]) -> List[Tuple[Node, Node, Capacity]]:
    """
    Extracts edges with capacities from the capacity matrix.
    
    Args:
        capacity_matrix: Matrix representing edge capacities
        nodes: List of all nodes in the network
        
    Returns:
        List of tuples containing (source, target, capacity)
    """
    edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if capacity_matrix[i][j] > 0:
                edges.append((nodes[i], nodes[j], capacity_matrix[i][j]))
    return edges 