import sqlite3

def func():

    conn = sqlite3.connect("your_database_file_full_path")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.name AS table_name,
            p.name AS column_name,
            p.type AS data_type
        FROM sqlite_master m
        JOIN pragma_table_info(m.name) p
        WHERE m.type = 'table'
        AND m.name NOT LIKE 'sqlite_%'
        ORDER BY m.name, p.cid;
    """)

    rows = cursor.fetchall()

    results = []
    current_group = None

    for row in rows:
        table_name = row[0]
        column_name = row[1]

        if current_group is None or table_name != current_group[0]:
            current_group = [table_name, column_name]
            results.append(current_group)
        else:
            current_group.append(column_name)

    conn.close()

    return results


if __name__ == "__main__":
    print(func())