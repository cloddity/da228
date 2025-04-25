from pinotdb import connect
import time
import math

host = "192.168.255.141"
port = 8099
table_name = "website_traffic_OFFLINE"

DECAY_RATE = 0.000001 

def get_decay_weight(timestamp_ms, now_ms):
    return math.exp(-DECAY_RATE * (now_ms - timestamp_ms))

def run_query(cursor, sql, description):
    print(f"\n{description}")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)

def main():
    conn = connect(host=host, port=port)
    cursor = conn.cursor()

    now_ms = int(time.time() * 1000)

    # Top 10 users with exponential decay applied to visit timestamps
    edw_query = f"""
        SELECT user_id,
               SUM(EXP(-{DECAY_RATE} * (CAST({now_ms} AS LONG) - timestamp))) AS decayed_score
        FROM {table_name}
        WHERE timestamp >= {now_ms - 60 * 60 * 1000}  -- last hour
        GROUP BY user_id
        ORDER BY decayed_score DESC
        LIMIT 10
    """
    run_query(cursor, edw_query, "Top 10 users by exponentially decaying visit score (last hour)")

    # Country visit weights using EDW
    edw_country_query = f"""
        SELECT country,
               SUM(EXP(-{DECAY_RATE} * (CAST({now_ms} AS LONG) - timestamp))) AS decayed_visits
        FROM {table_name}
        WHERE timestamp >= {now_ms - 24 * 60 * 60 * 1000}  -- last 24 hours
        GROUP BY country
        ORDER BY decayed_visits DESC
    """
    run_query(cursor, edw_country_query, "Country visit scores with EDW (last 24 hours)")

    # Browser popularity with EDW
    edw_browser_query = f"""
        SELECT browser,
               SUM(EXP(-{DECAY_RATE} * (CAST({now_ms} AS LONG) - timestamp))) AS weighted_popularity
        FROM {table_name}
        WHERE timestamp >= {now_ms - 24 * 60 * 60 * 1000}
        GROUP BY browser
        ORDER BY weighted_popularity DESC
    """
    run_query(cursor, edw_browser_query, "Browser popularity with EDW (last 24 hours)")

if __name__ == "__main__":
    main()
