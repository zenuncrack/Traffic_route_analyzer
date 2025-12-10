
import pulp

def solve_routing(nodes, edges, source, sink, demand):
    prob = pulp.LpProblem("TrafficRouting", pulp.LpMinimize)

    flow_vars = {}
    for e in edges:
        key = (e["from"], e["to"])
        flow_vars[key] = pulp.LpVariable(f"flow_{e['from']}_{e['to']}", lowBound=0)

    prob += pulp.lpSum(
        e["cost"] * flow_vars[(e["from"], e["to"])]
        for e in edges
    )

    for e in edges:
        prob += flow_vars[(e["from"], e["to"])] <= e["capacity"]

    for n in nodes:
        inflow = pulp.lpSum(flow_vars[(u, v)] for (u, v) in flow_vars if v == n)
        outflow = pulp.lpSum(flow_vars[(u, v)] for (u, v) in flow_vars if u == n)

        if n == source:
            prob += outflow - inflow == demand
        elif n == sink:
            prob += inflow - outflow == demand
        else:
            prob += inflow == outflow

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        return {"status": "Not Optimal"}

    flows = []
    for (u, v) in flow_vars:
        amt = pulp.value(flow_vars[(u, v)])
        if amt > 0.0001:
            flows.append({"from": u, "to": v, "flow": float(amt)})

    return {
        "status": "Optimal",
        "total_cost": float(pulp.value(prob.objective)),
        "flows": flows,
    }
