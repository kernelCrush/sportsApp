import sqlite3
import argparse
from prettytable import PrettyTable

def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def format_field_name(field_name):
    return ' '.join(word.capitalize() for word in field_name.split('_'))

def list_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    columns = [format_field_name(description[0]) for description in cursor.description if 'id' not in description[0]]

    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        filtered_row = [row[i] for i, desc in enumerate(cursor.description) if 'id' not in desc[0]]
        table.add_row(filtered_row)

    print(table)

def search_by_name(conn, search_input):

    try:
        table_name, name = search_input.split(':')
    except ValueError:
        print("Invalid search format. Use 'type:search_term'")
        return

    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE "
    if 'player' in table_name.lower():
        query+= "player_name LIKE ?"
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

def oldest_active_player(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, player_birthday FROM Players ORDER BY player_birthday ASC LIMIT 1")
    row = cursor.fetchone()

    table = PrettyTable(["Player Name", "Birthday"])
    table.add_row(row)

    print(table)

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
    cursor.execute("SELECT user_password FROM Users WHERE user_name = ?", (username,))
    result = cursor.fetchone()
    if result and result[0] == password:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Sports Management CLI")
    parser.add_argument("--list",  metavar='<Name>', type=str, help='List data of players, teams, etc.')
    parser.add_argument('--search', metavar='<type:input>', type=str, help='Search player/team/sport by name')
    parser.add_argument("--username", metavar='<Username>', type=str, help="your username")
    parser.add_argument("--password", metavar='<Password>', type=str, help="your password")
    parser.add_argument('--stats', metavar='STAT_TYPE', type=str, help='Type of statistic (e.g., teams_wins, oldest_player, highest_scorer_stadium)')
    parser.add_argument('--number', type=int, help='Numerical parameter for certain stats (e.g. win count for teams_wins)')
    parser.add_argument('--param', type=str, help='Additional parameter for certain stats')

    args = parser.parse_args()

    conn = connect_db("sports.db")

    # Check for username and password
    if not args.username or not args.password:
        print("Username and password required")
        return

    # Verify login credentials
    if not check_login(conn, args.username, args.password):
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
    
    conn.close()

if __name__ == "__main__":
    main()
