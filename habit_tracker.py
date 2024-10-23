import sqlite3
from habit import Habit
from datetime import datetime

class Habit_Tracker:
    def __init__(self,db_string):
        self.conn = sqlite3.connect(db_string)
        self.habits = []

    def create_table(self):
        self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS habits
        (habitID INTEGER primary key not null, name TEXT, date_created TIMESTAMP, periodicity TEXT, longest_streak INTEGER, current_streak INTEGER, last_update TIMESTAMP)''')
        self.conn.commit()

    def load_habits(self):
        #connect to database and retrieve habit data
        habit_data =self.conn.cursor().execute("SELECT name,date_created,periodicity,longest_streak,current_streak,last_update FROM habits;").fetchall()
        #instantiate habit objects and fill with data
        for data in habit_data:
            self.habits.append(Habit(data[0],datetime.strptime(data[1],"%Y-%m-%d %H:%M:%S.%f"),data[2],data[3],data[4],datetime.strptime(data[5],"%Y-%m-%d %H:%M:%S.%f")))
        for habit in self.habits:
            #updates all habits to make sure streaks are correctly stored
            habit.check_streaks(datetime.now())
            habit.update_longest_streak()
            
    def add_habit(self,habit_name: str,periodicity: str):
        #adds habit data to the array of habits
        current_date = datetime.now()
        self.habits.append(Habit(habit_name,current_date,periodicity,0,0, current_date))
        #adds new habit to database
        self.conn.cursor().execute("INSERT INTO habits (name,date_created,periodicity,longest_streak,current_streak,last_update) VALUES (?,?,?,?,?,?)", (habit_name, current_date, periodicity, 0, 0, current_date))
        self.conn.commit()

    def view_habits(self):
        #returns a string of the details of all habits
        return "\n".join([f"{i+1}. {habit.habit_to_string()}" for i, habit in enumerate(self.habits)])

    def view_habit_names(self):
        #returns the names of all habits
        return "\n".join([f"{i+1}. {habit.get_name()}" for i, habit in enumerate(self.habits)])

    def view_longest_streak(self):
        #searches through all habits to find what the longest streak is
        longest_streak_length = max(habit.get_streak() for habit in self.habits)
        #searches through all habits to find the ones that have a streak equal to the longest streak
        longest_streak_habits = filter(lambda habit: habit.get_streak() == longest_streak_length, self.habits)
        #returns a string of all habits with the longest streak
        return '\n'.join(map(lambda habit: habit.habit_to_string(),longest_streak_habits))

    def view_habits_interval(self,periodicity):
            #searches through all habits to find the ones with periodicity equal to the one chosen by the user
        filtered_habits = filter(lambda habit: habit.get_periodicity() == periodicity, self.habits)
            #returns a string with all the habits of the chosen periodicity
        return '\n'.join(map(lambda habit: habit.habit_to_string(), filtered_habits))

    def view_specific_habit(self,choice):
        index = int(choice) - 1
        #Finds the position of the one that corresponds to the chosen number, then returns the data of the habit in t he position
        if index >=0 and index <len(self.habits):
            return self.habits[index].habit_to_string()

    def update_habit(self,choice):
        index = int(choice) - 1
        #Finds the position of the corresponding habit, and updates the streak of the habit in the list, as well as in the database
        if index >=0 and index <len(self.habits):
            self.habits[index].update_streak(datetime.now())
            self.conn.cursor().execute("UPDATE habits SET current_streak = ?, last_update = ? WHERE name = ?", (self.habits[index].get_streak(),self.habits[index].get_last_update(),self.habits[index].get_name()))
            self.conn.commit()

    def delete_habit(self,choice):
        index = int(choice) - 1
        #Finds the position of the chosen habit, and then deletes the habits data from the database, as well as from the list
        if index>=0 and index <len(self.habits):
            self.conn.cursor().execute("DELETE FROM habits WHERE name = ? AND periodicity = ?",(self.habits[index].get_name(),self.habits[index].get_periodicity()))
            self.conn.commit()
            del self.habits[index]
