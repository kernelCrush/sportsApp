import sqlite3
import argparse
from prettytable import PrettyTable

# =====================varun====================================


def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn


def format_field_name(field_name):
    return ' '.join(word.capitalize() for word in field_name.split('_'))


# list table records
def list_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    columns = [format_field_name(description[0]) for description in cursor.description if 'id' not in description[0]]
    # columns = [format_field_name(description[0]) for description in cursor.description]

    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        filtered_row = [row[i] for i, desc in enumerate(cursor.description) if 'id' not in desc[0]]
        # filtered_row = [row[i] for i, desc in enumerate(cursor.description)]
        table.add_row(filtered_row)

    print(table)


# 1. view individual player/team stats
def search_by_name(conn, search_input):
    try:
        table_name, name = search_input.split(':')
    except ValueError:
        print("Invalid search format. Use 'type:search_term'")
        return

    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE "
    if 'player' in table_name.lower():
        query += "player_name LIKE ?"
    elif 'team' in table_name.lower():
        query += "team_name LIKE ?"
    elif 'sport' in table_name.lower():
        query += "sport_name LIKE ?"
    else:
        print("Invalid data to search")
        return

    cursor.execute(query, (f'%{name}%',))
    rows = cursor.fetchall()

    columns = [format_field_name(description[0]) for description in cursor.description if 'id' not in description[0]]
    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        filtered_row = [row[i] for i, desc in enumerate(cursor.description) if 'id' not in desc[0]]
        table.add_row(filtered_row)

    print(table)


def teams_with_wins_over(conn, win_count):
    cursor = conn.cursor()
    cursor.execute("SELECT team_name, num_win FROM Teams WHERE num_win > ?", (win_count,))
    rows = cursor.fetchall()

    table = PrettyTable(["Team Name", "Wins"])
    for row in rows:
        table.add_row(row)

    print(table)


# query oldest active player
def oldest_active_player(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, player_birthday FROM Players ORDER BY player_birthday ASC LIMIT 1")
    row = cursor.fetchone()

    table = PrettyTable(["Player Name", "Birthday"])
    table.add_row(row)

    print(table)


# query best scoring player in a paticular stadium(sorting)
def highest_scoring_player_in_stadium(conn, stadium_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.player_name, p.player_score, s.stad_name
        FROM Players p
        JOIN Matches m ON p.player_id = m.referee_id
        JOIN Stadium s ON m.stad_id = s.stad_id
        WHERE s.stad_name = ?
        ORDER BY p.player_score DESC
        LIMIT 1
        """, (stadium_name,))
    row = cursor.fetchone()

    table = PrettyTable(["Player Name", "Score", "Stadium"])
    table.add_row(row)

    print(table)


def check_login(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT user_password,user_right FROM Users WHERE user_name = ?", (username,))
    result = cursor.fetchone()
    if result and result[0] == password:
        return True, result[1]
    return False, ""
# =========================================================================↑


# ------------------------Jingjing----------------------------------------
# Insert into tables
def insert_tuple(conn, table_name, *para):
    if table_name == "Users":  # (conn,"Users", user_name, user_right, user_password)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (user_name, user_right, points, user_password) VALUES (?,?,?,?)", (para[0], para[1], 0, para[2],))
        conn.commit()
        print("-----To show the insert result: ")
        list_table(conn, "Users")


# Delete from tables
def delete_tuple(conn, delete_input):
    try:
        table_name, column, value = delete_input.split(':')
    except ValueError:
        print("Invalid format. Use 'table name:attribute name:attribute value'")
        return

    cursor = conn.cursor()        # DELETE FROM Team WHERE team_name = '123';
    cursor.execute(f"DELETE FROM {table_name} WHERE {column}='{value}'")
    conn.commit()
    print("-----To show the delete result: ")
    list_table(conn, table_name)


# Update tuple for certain table
def update_tuple(conn, update_input):
    try:
        match_name_temp, live_score = update_input.split('=')
        match_name = match_name_temp.replace('_', ' ')
    except ValueError:
        print("Invalid format. Use 'match name=score'")
        return

    cursor = conn.cursor()
    cursor.execute(f'''UPDATE Matches
        SET live_score = '{live_score}'
        WHERE match_name = '{match_name}';
        ''')
    conn.commit()
    print("-----To show the update result: ")
    list_table(conn, "Matches")

# query tuples from tables.
def query_table(conn, query_sql):
    cursor = conn.cursor()
    cursor.execute(query_sql)
    rows = cursor.fetchall()

    columns = [format_field_name(description[0]) for description in cursor.description]

    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        filtered_row = [row[i] for i, desc in enumerate(cursor.description)]
        table.add_row(filtered_row)

    print(table)
    return rows

# user signup
def user_signup(conn):
    user_name = input("what is your username: ")
    user_password = input("what is your password: ")
    user_right = input("what is your position(user/player/coach/admin/referee): ")
    insert_tuple(conn, "Users", user_name, user_right, user_password)


# Search stadium details
def search_stadium(conn,stadium_name):
    query_sql = f"SELECT stad_id, stad_name, capacity, address, stad_area, stad_status, livecapacity FROM Stadium WHERE stad_name = '{stadium_name}'"
    print(query_sql)
    query_table(conn, query_sql)


# Booking tickets
def ticket_booking(conn,match_name):
    cursor = conn.cursor()
    cursor.execute("SELECT match_name FROM Matches WHERE match_status = 'Scheduled'")
    rows = cursor.fetchall()
    match_names = [row[0] for row in rows]
    while match_name not in match_names:
        print("You entered incorrect match name, please select one from the following Matches: ")
        print(match_names)
        match_name = input()

    cursor.execute(f"SELECT ticketNum FROM Matches WHERE match_name = '{match_name}'")
    rows = cursor.fetchone()
    ticket_left = (rows[0])

    ticket_num = input(f"There are {ticket_left} tickets left for match ‘{match_name}', how many do you want: ")

    cursor.execute("")


# ---------------------------------------------------------------------------↑


def main():
    # ==============================varun=========================
    parser = argparse.ArgumentParser(description="Sports Management CLI")
    parser.add_argument("--list", metavar='<Name>', type=str, help='List data of players, teams, etc.')
    parser.add_argument('--search', metavar='<type:input>', type=str, help='Search player/team/sport by name')
    parser.add_argument("--username", metavar='<Username>', type=str, help="your username")
    parser.add_argument("--password", metavar='<Password>', type=str, help="your password")
    # 6.Some queries that return interesting insights (sorting)
    parser.add_argument('--stats', metavar='STAT_TYPE', type=str,
                        help='Type of statistic (e.g., teams_wins, oldest_player, highest_scorer_stadium)')
    parser.add_argument('--number', type=int,
                        help='Numerical parameter for certain stats (e.g. win count for teams_wins)')
    parser.add_argument('--param', type=str, help='Additional parameter for certain stats')
    # ============================================================↑
    # -----------------------------Jingjing----------------------
    # 1.2 Delete individual player/team stats
    # command: python .\sports_cli.py --username Leah --password leah123 --delete Users:user_name:li
    parser.add_argument('--delete', type=str, help='Delete tuple from tables(table name:attribute name:attribute value)')

    # 2.Ability to input live scores for games, and view the same by multiple users in real-time 3.Only referee have the right to change the live score of certain match.
    # command: python .\sports_cli.py --username Leah --password leah123 --updatescore El_Clasico=0-1
    parser.add_argument('--updatescore', type=str, help='Update live score of certain match(match name=score)')

    # 4.Automatic schedule creator for match
    # parser.add_argument('--updatescore', type=str, help='Update live score of certain match(match name=score)')

    # 5.View stadium details
    # python .\sports_cli.py --username li --password 123456 --stadium "Yankee Stadium"
    parser.add_argument('--stadium', type=str, help='Search ditails of stadium(stadium name)')

    # 7. Booking a ticket
    parser.add_argument('--ticket', type=str, help='Book tickets for certain match(match name)')
    # -----------------------------------------------------------↑

    args = parser.parse_args()

    conn = connect_db("sports.db")

    # to add user_right checking for the permission of DB operations
    usr_right_temp = ""

    # Check for username and password
    if not args.username or not args.password:
        print("Username and password required")
        signup = input("If don't have an account, sign up right now(y/n)")
        if signup == 'y':
            user_signup(conn)
            print("sign up successfully, please login again")
            return
        else:
            print("Please input your username using --username and password using --password")
            return

    # Verify login credentials
    usr_validation, usr_right = check_login(conn, args.username, args.password)
    usr_right_temp = usr_right
    if not usr_validation:
        print("Invalid username or password")
        return

    if args.list:
        valid_tables = ["Players", "Teams", "Stadium", "Sports", "Matches"]
        if args.list.capitalize() in valid_tables:
            list_table(conn, args.list.capitalize())
        else:
            print(f"Invalid table name. Valid options are: {', '.join(valid_tables)}")

    elif args.search:
        search_by_name(conn, args.search)

    elif args.stats:
        if args.stats == "wins" and args.number is not None:
            teams_with_wins_over(conn, args.number)
        elif args.stats == "oldest_player":
            oldest_active_player(conn)
        elif args.stats == "highest_scorer_stadium" and args.param:
            highest_scoring_player_in_stadium(conn, args.param)
        else:
            print("Invalid stats type or missing parameters")

# ----------------------------Jingjing-------------------------------------↓
    elif args.delete:
        delete_tuple(conn, args.delete)

    elif args.updatescore:
        if usr_right_temp == "referee":
            update_tuple(conn, args.updatescore)
        else:
            print("Only referee can update live scores, you have no permission")
        return

    elif args.stadium:
        search_stadium(conn, args.stadium)

    elif args.ticket:
        ticket_booking(conn,args.ticket, args.username)
# -------------------------------------------------------------------------↑
    conn.close()


if __name__ == "__main__":
    main()
