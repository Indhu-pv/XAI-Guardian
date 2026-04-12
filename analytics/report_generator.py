import pandas as pd
import io

def generate_csv_report(df):
    """
    Generate CSV for download.
    """
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer.getvalue()

def generate_text_audit(metrics):
    """
    Generate text report for auditing.
    """
    lines = [
        "========================================",
        "      XAI GUARDIAN AUDIT REPORT",
        "========================================",
        f"Overall Approval Rate: {metrics['overall_rate']*100:.1f}%",
        "",
        "--- DEMOGRAPHIC METRICS ---",
        f"Male Approval Rate: {metrics['gender_rates']['Male']*100:.1f}%",
        f"Female Approval Rate: {metrics['gender_rates']['Female']*100:.1f}%",
        f"Urban Approval Rate: {metrics['location_rates']['Urban']*100:.1f}%",
        f"Rural Approval Rate: {metrics['location_rates']['Rural']*100:.1f}%",
        "",
        "--- ALERTS ---"
    ]
    for alert in metrics['alerts']:
        lines.append(f"[{alert['level']}] {alert['message']}")
        lines.append(f"-> Action: {alert['action']}")
        lines.append("")
        
    return "\n".join(lines)
