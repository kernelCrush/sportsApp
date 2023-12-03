CREATE TABLE Users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(20),
	user_right VARCHAR(10),
	points INT,
	user_password VARCHAR(15)
);

CREATE TABLE Players (
	player_id INT AUTO_INCREMENT PRIMARY KEY,
	player_name VARCHAR(20),
	player_score INT,
	player_birthday DATETIME,
	origin_place VARCHAR(20),
	height DECIMAL(4,2),
	sex VARCHAR(10),
	weight INT,
	FOREIGN KEY (player_id) REFERENCES users(user_id)
);

CREATE TABLE Teams (
	team_id INT AUTO_INCREMENT PRIMARY KEY,
	team_name VARCHAR(20),
	coach_id INT,
	orig_place VARCHAR(20),
	orig_year INT,
	active_year INT,
	num_win INT,
	num_failure INT,
	FOREIGN KEY (coach_id) REFERENCES Users(user_id)
);

CREATE TABLE Stadium (
	stad_id INT AUTO_INCREMENT PRIMARY KEY,
	stad_name VARCHAR(20),
	capacity INT,
	address VARCHAR(30),
	stad_area VARCHAR(10),
	stad_status VARCHAR(10),
	livecapacity INT
);

CREATE TABLE Sports (
	sport_id INT AUTO_INCREMENT PRIMARY KEY,
	sport_name VARCHAR(20),
	instuction TEXT,
	match_duration INT
);

CREATE TABLE Matches (
	match_id INT AUTO_INCREMENT PRIMARY KEY,
	match_name VARCHAR(20),
	stad_id INT,
	sport_id INT,
	match_time DATE,
	ticketNum INT,
	ticket_price INT,
	live_score VARCHAR(20),
	referee_id INT,
	match_status VARCHAR(20),
    home_team_id INT,
    away_team_id INT,
	FOREIGN KEY (stad_id) REFERENCES Stadium(stad_id),
	FOREIGN KEY (referee_id) REFERENCES Users(user_id),
	FOREIGN KEY (sport_id) REFERENCES Sports(sport_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id),
);

CREATE TABLE BookingHistory (
	match_id INT,
	user_id INT,
	order_time DATETIME,
	ticket_num INT,
	order_id INT AUTO_INCREMENT PRIMARY KEY,
	FOREIGN KEY (match_id) REFERENCES Matches(match_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE ParticipationRecord (
	user_id INT,
	match_id INT,
	live_socre INT DEFAULT 0,
	participant_type VARCHAR(15),
	PRIMARY KEY (user_id, match_id),
	FOREIGN KEY (match_id) REFERENCES Matches(match_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE HistoricalFacts (
	fact_id INT AUTO_INCREMENT PRIMARY KEY,
	content TEXT,
	publish_time DATETIME,
	author_id INT,
	FOREIGN KEY (author_id) REFERENCES Users(user_id)
);

INSERT INTO Users (user_id, user_name, user_right, points, user_password) VALUES
(1, 'AlexCoach', 'coach', 100, 'alexPass'),
(2, 'RefSmith', 'referee', 50, 'refPass123'),
(3, 'Leah', 'user', 75, 'leah123'),
(4, 'Varun', 'user', 80, 'var4796'),
(5, 'LukeAdmin', 'admin', 60, 'lukeAdmin88');

INSERT INTO Players (player_id, player_name, player_score, player_birthday, origin_place, height, sex, weight) VALUES
(4, 'Cristiano Ronaldo', 760, '1985-02-05', 'Portugal', 1.87, 'Male', 83),
(6, 'Serena Williams', 23, '1981-09-26', 'United States', 1.75, 'Female', 70),
(7, 'LeBron James', 35000, '1984-12-30', 'United States', 2.06, 'Male', 113),
(8, 'Lionel Messi', 750, '1987-06-24', 'Argentina', 1.70, 'Male', 72),
(9, 'Roger Federer', 103, '1981-08-08', 'Switzerland', 1.85, 'Male', 85);

INSERT INTO Teams (team_id, team_name, coach_id, orig_place, orig_year, active_year, num_win, num_failure) VALUES
(NULL, 'Los Angeles Lakers', 1, 'Los Angeles', 1947, 76, 3385, 2306),
(NULL, 'New York Yankees', 1, 'New York', 1901, 122, 10837, 8389),
(NULL, 'FC Barcelona', 1, 'Barcelona', 1899, 124, 3100, 1102),
(NULL, 'Dallas Cowboys', 1, 'Dallas', 1960, 63, 520, 388),
(NULL, 'Boston Celtics', 1, 'Boston', 1946, 77, 3448, 2388);

INSERT INTO Stadium (stad_id, stad_name, capacity, address, stad_area, stad_status, livecapacity) VALUES
(1, 'Camp Nou', 99354, 'Arístides Maillol, 12, 08028 Barcelona, Spain', 'East', 'Active', 99354),
(2, 'Yankee Stadium', 47309, '1 E 161 St, The Bronx, NY 10451, United States', 'North', 'Active', 47309),
(3, 'AT&T Stadium', 80000, '1 AT&T Way, Arlington, TX 76011, United States', 'West', 'Active', 80000),
(4, 'Staples Center', 19068, '1111 S Figueroa St, Los Angeles, CA 90015, United States', 'South', 'Active', 19068),
(5, 'Fenway Park', 37755, '4 Jersey St, Boston, MA 02215, United States', 'Central', 'Active', 37755);

INSERT INTO Sports (sport_id, sport_name, instuction, match_duration) VALUES
(1, 'Soccer', 'Two teams of eleven players each compete to score by driving a ball into the opposing goal', 90),
(2, 'Basketball', 'Two teams of five players each compete to score points by shooting a ball through a hoop', 48),
(3, 'Baseball', 'Two teams alternate between batting and fielding, aiming to score runs', 180),
(4, 'Tennis', 'Players or teams compete on opposite sides of a net, trying to hit a ball onto the other player’s court', 120),
(5, 'American Football', 'Two teams compete to advance the ball into the opponent’s end zone to score points', 60);

INSERT INTO Matches (match_id, match_name, stad_id, sport_id, match_time, ticketNum, ticket_price, live_score, referee_id, match_status) VALUES
(1, 'El Clasico', 1, 1, '2023-11-20', 99354, 150, '0-0', 2, 'Scheduled'),
(2, 'NBA Finals Game 7', 4, 2, '2023-06-18', 19068, 200, '0-0', 2, 'Scheduled'),
(3, 'World Series Game 5', 2, 3, '2023-10-30', 47309, 100, '0-0', 2, 'Scheduled'),
(4, 'Wimbledon Men’s Final', 3, 4, '2023-07-14', 15000, 500, '0-0', 2, 'Scheduled'),
(5, 'Super Bowl', 3, 5, '2024-02-04', 80000, 1000, '0-0', 2, 'Scheduled');

INSERT INTO BookingHistory (match_id, user_id, order_time, ticket_num, order_id) VALUES
(1, 3, '2023-10-01 10:30:00', 2, NULL),
(2, 3, '2023-05-01 15:00:00', 1, NULL),
(3, 4, '2023-10-10 12:00:00', 4, NULL),
(4, 4, '2023-06-30 16:45:00', 2, NULL),
(5, 5, '2024-01-20 09:20:00', 3, NULL);

INSERT INTO ParticipationRecord (user_id, match_id, live_socre, participant_type) VALUES
(3, 1, 0, 'spectator'),
(4, 2, 0, 'participant'),
(1, 3, 0, 'coach'),
(2, 4, 0, 'referee'),
(5, 5, 0, 'admin');

INSERT INTO HistoricalFacts (fact_id, content, publish_time, author_id) VALUES
(1, 'The New York Yankees have won 27 World Series championships, the most in MLB history.', '2023-04-10 14:00:00', 5),
(2, 'Michael Jordan led the Chicago Bulls to six NBA championships in the 1990s.', '2023-04-12 10:30:00', 5),
(3, 'FC Barcelona has won the UEFA Champions League five times.', '2023-04-15 17:20:00', 5),
(4, 'The FIFA World Cup is the most prestigious soccer tournament in the world.', '2023-04-18 13:45:00', 5),
(5, 'Serena Williams has won 23 Grand Slam singles titles, the most by any player in the Open Era.', '2023-04-20 16:30:00', 5);
