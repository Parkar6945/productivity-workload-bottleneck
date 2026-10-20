import json
from collections import defaultdict

class WorkloadAnalyticsEngine:
    def __init__(self, data_path="productivity_workload_data.json"):
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def analyze_bottlenecks(self):
        total_staff = len(self.data)
        burned_out_staff = [e for e in self.data if e["burnout_risk_score"] >= 65]
        overworked_staff = [e for e in self.data if e["weekly_hours_logged"] > 48]

        avg_hours = sum(e["weekly_hours_logged"] for e in self.data) / total_staff
        avg_prod = sum(e["effective_productivity_score"] for e in self.data) / total_staff
        avg_rework = sum(e["rework_rate_pct"] for e in self.data) / total_staff

        # Team Aggregates
        teams = defaultdict(lambda: {
            "count": 0, "total_hours": 0, "total_prod": 0, "total_burnout": 0, "total_rework": 0, "total_latency": 0
        })

        for e in self.data:
            t = e["team"]
            teams[t]["count"] += 1
            teams[t]["total_hours"] += e["weekly_hours_logged"]
            teams[t]["total_prod"] += e["effective_productivity_score"]
            teams[t]["total_burnout"] += e["burnout_risk_score"]
            teams[t]["total_rework"] += e["rework_rate_pct"]
            teams[t]["total_latency"] += e["blocker_latency_hrs"]

        team_breakdown = []
        for t, s in teams.items():
            n = s["count"]
            mean_hrs = s["total_hours"] / n
            mean_prod = s["total_prod"] / n
            mean_burnout = s["total_burnout"] / n
            mean_rework = s["total_rework"] / n

            status = "HEALTHY"
            intervention = "Maintain current sprint pacing."
            if mean_hrs > 48 or mean_burnout > 55:
                status = "BURNOUT ZONE (Productivity Penalty)"
                intervention = "Cap WIP tasks, redistribute epics, and institute meeting-free focus days."
            elif mean_rework > 12:
                status = "HIGH QUALITY DEFICIT"
                intervention = "Strengthen peer QA/review gates to mitigate high defect rework."

            team_breakdown.append({
                "team": t,
                "headcount": n,
                "avg_weekly_hours": round(mean_hrs, 1),
                "avg_productivity_score": round(mean_prod, 1),
                "avg_burnout_index": round(mean_burnout, 1),
                "avg_rework_pct": round(mean_rework, 1),
                "status": status,
                "intervention": intervention
            })

        team_breakdown.sort(key=lambda x: x["avg_weekly_hours"], reverse=True)

        # Hour buckets to chart the classical inverted-U / diminishing returns curve
        # Buckets: "<40 hrs", "40-45 hrs", "45-50 hrs", "50-55 hrs", "55+ hrs"
        buckets = {
            "<40 hrs": {"hours": 0, "prod": [], "rework": []},
            "40-45 hrs": {"hours": 0, "prod": [], "rework": []},
            "45-50 hrs": {"hours": 0, "prod": [], "rework": []},
            "50-55 hrs": {"hours": 0, "prod": [], "rework": []},
            "55+ hrs": {"hours": 0, "prod": [], "rework": []}
        }

        for e in self.data:
            hrs = e["weekly_hours_logged"]
            b_key = "<40 hrs" if hrs < 40 else "40-45 hrs" if hrs <= 45 else "45-50 hrs" if hrs <= 50 else "50-55 hrs" if hrs <= 55 else "55+ hrs"
            buckets[b_key]["prod"].append(e["effective_productivity_score"])
            buckets[b_key]["rework"].append(e["rework_rate_pct"])

        curve_data = []
        for k, v in buckets.items():
            mean_p = sum(v["prod"]) / len(v["prod"]) if v["prod"] else 0
            mean_r = sum(v["rework"]) / len(v["rework"]) if v["rework"] else 0
            curve_data.append({
                "workload_bracket": k,
                "sample_size": len(v["prod"]),
                "avg_productivity": round(mean_p, 1),
                "avg_rework_pct": round(mean_r, 1)
            })

        return {
            "metrics": {
                "total_staff": total_staff,
                "avg_weekly_hours": round(avg_hours, 1),
                "avg_productivity_score": round(avg_prod, 1),
                "avg_rework_rate": round(avg_rework, 1),
                "burnout_risk_headcount": len(burned_out_staff),
                "overworked_ratio_pct": round((len(overworked_staff) / total_staff) * 100, 1)
            },
            "diminishing_returns_curve": curve_data,
            "teams": team_breakdown,
            "top_bottlenecks": sorted(burned_out_staff, key=lambda x: x["weekly_hours_logged"], reverse=True)[:8]
        }

if __name__ == "__main__":
    eng = WorkloadAnalyticsEngine()
    print(eng.analyze_bottlenecks()["metrics"])
