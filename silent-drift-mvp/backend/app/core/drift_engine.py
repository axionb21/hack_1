from app.db.crud import get_recent_logs

def calculate_drift_status():
    logs = get_recent_logs(limit=100)
    
    if not logs:
        return {
            "overall_score": 0.0,
            "status": "WAITING_DATA",
            "input_drift": 0.0,
            "output_drift": 0.0,
            "confidence_drift": 0.0,
            "subgroup": "None",
            "alerts": ["Waiting for incoming predictions..."]
        }

    avg_conf = sum(l['confidence'] for l in logs) / len(logs)
    status = "STABLE"
    alerts = []

    if avg_conf < 0.3:
        status = "CRITICAL"
        alerts.append("Critical drop in model confidence.")
    elif avg_conf < 0.5:
        status = "WARNING"
        alerts.append("Confidence levels are degrading.")
    else:
        alerts.append("System operating within normal parameters.")

    return {
        "overall_score": 0.85,
        "status": status,
        "input_drift": 0.4,
        "output_drift": 0.6,
        "confidence_drift": round(avg_conf, 2),
        "subgroup": "category_B",
        "alerts": alerts
    }
