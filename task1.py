#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logistics network analysis application.
This script analyzes a logistics network to find maximum flow and bottlenecks.
"""

from task1.modules.edmonds_karp import edmonds_karp
from task1.modules.logistics_network import (
    build_logistics_network, 
    calculate_terminal_to_store_flow, 
    analyze_network,
    get_edges_from_matrix
)
from task1.modules.report_generator import generate_report, save_report


def main():
    """
    Main function to run the logistics network analysis.
    """
    print("Початок аналізу логістичної мережі...")
    
    # Build the logistics network
    nodes, node_indices, capacity_matrix = build_logistics_network()
    
    # Get edges with capacities for the report
    edges = get_edges_from_matrix(capacity_matrix, nodes)
    
    # Create super source and super sink for the analysis
    n = len(nodes)
    super_source = n
    super_sink = n + 1
    
    # Extend capacity matrix for super source and super sink
    extended_capacity = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Copy original capacity matrix
    for i in range(n):
        for j in range(n):
            extended_capacity[i][j] = capacity_matrix[i][j]
    
    # Connect super source to all terminals
    for t in ["Термінал 1", "Термінал 2"]:
        t_idx = node_indices[t]
        extended_capacity[super_source][t_idx] = 100  # High capacity
    
    # Connect all stores to super sink
    for s in [f"Магазин {i}" for i in range(1, 15)]:
        s_idx = node_indices[s]
        extended_capacity[s_idx][super_sink] = 100  # High capacity
    
    # Calculate maximum flow
    max_flow, flow_matrix, path_history = edmonds_karp(extended_capacity, super_source, super_sink)
    
    # Trim the flow matrix back to original size
    original_flow_matrix = [row[:n] for row in flow_matrix[:n]]
    
    # Calculate terminal to store flows through warehouses
    terminal_to_store_flows = calculate_terminal_to_store_flow(original_flow_matrix, node_indices)
    
    # Analyze the network
    analysis = analyze_network(capacity_matrix, original_flow_matrix, nodes, node_indices, path_history)
    
    # Generate report
    report = generate_report(max_flow, analysis, terminal_to_store_flows, nodes, node_indices, edges)
    
    # Save the report to a file
    save_report(report)
    
    print(f"Аналіз завершено. Максимальний потік: {max_flow} одиниць")
    print("- logistics_analysis_report.md (звіт з аналізом)")


if __name__ == "__main__":
    main() 