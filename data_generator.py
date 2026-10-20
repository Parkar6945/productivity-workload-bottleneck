import random
import json

TEAMS = ["Backend Platform", "Frontend Apps", "Data Engineering", "Customer Solutions", "Core Operations"]

def generate_workload_dataset(num_employees=150):
    random.seed(42)
    records = []

    for i in range(1, num_employees + 1):
        emp_id = f"WRK-{4000 + i}"
        team = random.choice(TEAMS)
        weekly_hours = random.randint(35, 68)
        overtime_hours = max(0, weekly_hours - 40)
        tasks_assigned = random.randint(12, 45)
        
        # Burnout threshold logic: As weekly hours exceed 48, productivity per hour diminishes, error rate escalates
        if weekly_hours <= 42:
            completion_rate = random.uniform(85, 98)
            code_review_latency_hrs = random.uniform(2, 6)
            error_rework_rate = random.uniform(2, 7)
            burnout_index = random.uniform(10, 30)
            productivity_score = random.uniform(80, 95)
        elif weekly_hours <= 50:
            completion_rate = random.uniform(75, 90)
            code_review_latency_hrs = random.uniform(5, 12)
            error_rework_rate = random.uniform(6, 14)
            burnout_index = random.uniform(35, 65)
            productivity_score = random.uniform(70, 85)
        else: # Severe Overwork Burnout
            completion_rate = random.uniform(50, 72)
            code_review_latency_hrs = random.uniform(12, 30)
            error_rework_rate = random.uniform(15, 35)
            burnout_index = random.uniform(70, 98)
            productivity_score = random.uniform(40, 65)

        records.append({
            "employee_id": emp_id,
            "team": team,
            "weekly_hours_logged": weekly_hours,
            "overtime_hours": overtime_hours,
            "tasks_assigned": tasks_assigned,
            "completion_rate_pct": round(completion_rate, 1),
            "rework_rate_pct": round(error_rework_rate, 1),
            "blocker_latency_hrs": round(code_review_latency_hrs, 1),
            "burnout_risk_score": round(burnout_index, 1),
            "effective_productivity_score": round(productivity_score, 1)
        })

    with open("productivity_workload_data.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print(f"Generated productivity data for {num_employees} employees.")

if __name__ == "__main__":
    generate_workload_dataset()
