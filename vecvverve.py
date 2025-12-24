import psycopg2
import pandas as pd
from io import StringIO
import datetime

# PostgreSQL connection details
db_config = {
    "host": "192.168.220.29",
    "database": "nguccreports",
    "user": "postgres",
    "password": "Avis!123",
    "port": "5432"
}

# Conference Report Query
query = """
SELECT
    c.startdate                     AS "Start Date",
    c.enddate                       AS "End Date",
    u.name                          AS "Agent",
    camp.name                       AS "Campaign",
    c.phonenumber                   AS "Conference Number",
    c.accountcode                   AS "Account Code",
    c.recordingfilename             AS "Recording File Name",
    TO_CHAR(make_interval(secs => c.confduration), 'HH24:MI:SS')
                                    AS "Conference Duration",
    c.customernumber                AS "Customer Number",
    c.hangupcause                   AS "Hangup Cause",
    c.confaccountcode               AS "Conference Account Code"
FROM cr_conf_log c
LEFT JOIN ct_user u        ON c.agentid = u.id
LEFT JOIN ct_campaign camp ON c.campid = camp.id
WHERE c.startdate >= '2025-12-19'
  AND c.startdate <= '2025-12-20'
ORDER BY c.startdate;
"""

try:
    # DB Connection
    conn = psycopg2.connect(**db_config)

    # Fetch data into DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    # CSV in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Dynamic filename
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"/tmp/conference_report_2019-01-01_to_2019-01-30_{current_time}.csv"

    # Write CSV to file
    with open(file_path, "w") as f:
        f.write(csv_buffer.getvalue())

    print(f"✅ Conference Report saved at: {file_path}")

except Exception as e:
    print(f"❌ Error: {e}")
