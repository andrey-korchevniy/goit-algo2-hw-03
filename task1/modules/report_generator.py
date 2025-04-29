#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Report generation for logistics network analysis.
"""

from typing import Dict, List, Tuple, Any
from tabulate import tabulate

# Type aliases
Node = str
NodeIndex = int
Flow = int
Capacity = int


def generate_report(max_flow: Flow, analysis: Dict[str, Any], 
                   terminal_to_store_flows: List[Tuple[Node, Node, Flow]], 
                   nodes: List[Node], node_indices: Dict[Node, NodeIndex], 
                   edges: List[Tuple[Node, Node, Capacity]]) -> str:
    """
    Generates a detailed report of the logistics network analysis.
    
    Args:
        max_flow: Maximum flow value
        analysis: Analysis results
        terminal_to_store_flows: Flow between terminals and stores
        nodes: List of all nodes in the network
        node_indices: Mapping of node names to indices
        edges: List of edges with capacities
        
    Returns:
        String containing the formatted report
    """
    report = []
    
    # Overview
    report.append("# Аналіз логістичної мережі\n")
    report.append(f"Максимальний потік товарів: {max_flow} одиниць\n")
    
    # Terminal-to-Store flows table
    report.append("## Таблиця потоків між терміналами та магазинами\n")
    
    # Prepare data for table
    table_data = []
    headers = ["Термінал", "Магазин", "Фактичний Потік (одиниці)"]
    
    for terminal, store, flow in terminal_to_store_flows:
        table_data.append([terminal, store, flow])
    
    report.append(tabulate(table_data, headers=headers, tablefmt="grid"))
    report.append("\n\n")
    
    # Analysis according to requirements
    report.append("## Аналіз отриманих результатів\n")
    
    # Question 1: Which terminals provide the largest flow to stores?
    terminal_flows = {}
    for terminal, outflow in analysis["terminal_outflows"].items():
        terminal_flows[terminal] = outflow
    
    max_flow_terminals = [terminal for terminal, flow in terminal_flows.items() 
                         if flow == max(terminal_flows.values())]
    
    report.append(f"1. Найбільший потік товарів до магазинів забезпечують: {', '.join(max_flow_terminals)} (потік: {max(terminal_flows.values())} одиниць).\n\n")
    
    # Question 2: Which routes have the lowest capacity and how it affects overall flow?
    low_capacity_routes = sorted([(source, target, capacity) for source, target, capacity in edges], 
                                key=lambda x: x[2])[:4]  # Get 4 routes with lowest capacity
    
    low_capacity_text = ", ".join([f"{source} -> {target}" for source, target, _ in low_capacity_routes])
    lowest_capacity = low_capacity_routes[0][2] if low_capacity_routes else 0
    
    report.append(f"2. Найменшу пропускну здатність мають маршрути: {low_capacity_text} (пропускна здатність: {lowest_capacity}). "
                  f"Це обмежує загальний потік, оскільки ці маршрути є вузькими місцями мережі.\n\n")
    
    # Question 3: Which stores received the least goods and can their supply be increased?
    store_inflows = analysis["store_inflows"]
    lowest_inflow_stores = [store for store, inflow in store_inflows.items() 
                           if inflow == min(store_inflows.values())]
    
    report.append(f"3. Найменше товарів отримали магазини: {', '.join(lowest_inflow_stores)} (отримано: {min(store_inflows.values())} одиниць). "
                  f"Збільшити постачання можна, якщо підвищити пропускну здатність вузьких маршрутів, що ведуть до цих магазинів.\n\n")
    
    # Question 4: Are there bottlenecks that can be eliminated to improve network efficiency?
    bottleneck_text = ", ".join([f"{source} -> {target}" for source, target, _ in analysis["bottlenecks"]])
    
    report.append(f"4. Вузькі місця: {bottleneck_text}. Усунення цих обмежень дозволить збільшити загальний потік та покращити ефективність мережі.\n")
    
    return "\n".join(report)


def save_report(report: str, filename: str = "logistics_analysis_report.md") -> None:
    """
    Saves the generated report to a file.
    
    Args:
        report: Report content
        filename: Name of the output file
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Звіт збережено у файлі: {filename}") 