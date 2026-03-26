import sqlite3
import os
from src.database import DB_PATH

def get_stats():
    """Fetches stats from the database."""
    if not DB_PATH.exists():
        return "No database found."
        
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    
    # Total Uploads
    cur.execute("SELECT COUNT(*) FROM uploads WHERE status = 'success'")
    success_count = cur.fetchone()[0]
    
    # Recent Uploads
    cur.execute("SELECT date, title FROM uploads ORDER BY date DESC LIMIT 5")
    recent = cur.fetchall()
    
    # Quota usage (from log if exists)
    quota = "Unknown"
    if os.path.exists("quota_usage.log"):
        with open("quota_usage.log", "r") as f:
            lines = f.readlines()
            quota = f"{len(lines) * 1600} units used today" # Approximate
            
    conn.close()
    
    # Format output
    output = f"""
=========================================
YouTube Automation Dashboard
=========================================
Success Count: {success_count}
Quota Status:  {quota}

Recent Uploads:
"""
    for date, title in recent:
        output += f"- [{date}] {title}\n"
    
    output += "========================================="
    return output

if __name__ == "__main__":
    print(get_stats())
 Aurora Dashboard v1.0
