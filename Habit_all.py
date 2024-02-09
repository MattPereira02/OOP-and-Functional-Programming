import sqlite3
from datetime import datetime
import os.path

class Habit:
    def __init__(self,name,created_date,periodicity,longest_streak,current_streak,last_update_date):
        #initialize all variables of what we consider to be a habit
        self.name = name
        self.created_date=created_date
        self.periodicity = periodicity
        self.longest_streak = longest_streak
        self.current_streak = current_streak
        self.last_update_date = last_update_date

    def __repr__(self):
        return f"Habit('{self.name}','{self.created_date}','{self.periodicity}')"
    
    def add_log(self,date):
        self.log.append(date)

    def update_streak(self,date):
        #checks if the habit is daily or weekly,and if it has been long enough since the last update to update again
        if self.periodicity == "Daily":
            if self.last_update_date and (date - self.last_update_date).days ==1:
                self.current_streak += 1
            else:
                self.current_streak = 1
        elif self.periodicity == "Weekly":
            if self.last_update_date and (date - self.last_update_date).days ==7:
                self.current_streak +=1
            else:
                self.current_streak = 1
        #checks if the current streak is longer than the longest streak, and updates the longest streak if it is
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        #sets the last update date to be the date of the update
        self.last_update_date = date

    def check_streaks(self,date):
        if self.periodicity == "Daily":
            if self.last_update_date and (date - self.last_update_date).days > 1:
                self.current_streak = 0
        elif self.periodicity == "Weekly":
            if self.last_update_date and (date - self.last_update_date).days > 7:
                self.current_streak = 0

    def get_streak(self):
        #returns the current streak of the habit
        return self.current_streak

    def habit_to_string(self):
        #returns a string with the details of the habit
        c_date = datetime.strftime(self.created_date,"%d-%m-%Y")
        return f"Habit: {self.name}, Created: {c_date}, Period: {self.periodicity}, Current streak: {self.current_streak}, Longest streak: {self.longest_streak}"

    def get_name(self):
        #returns habit name
        return self.name

    def get_periodicity(self):
        #returns habit periodicity
        return self.periodicity
    
    def get_last_update(self):
        #returns last update date
        return self.last_update_date

    def update_longest_streak(self):
        #checks if the current streak is longer than the longest streak, and if it is, set the longest streak to equal the current streak
        if self.current_streak>self.longest_streak:
            self.longest_streak = self.current_streak

class Habit_UI:
    def print_menu(self):
        #prints the menu of options that the user can choose from
        print("1. View all habits\n2. Add new habit\n3. View longest streak\n4. View a specific habits data\n5. View all habits of the same interval\n6. Update the streak of a habit\n7. Delete a habit\n0. Exit program\n")

    def get_option(self):
        #returns the option chosen by the user
            option = input("Please enter the number of the option you would like to choose: ")
            if option.isdigit():
                if int(option)<=7 and int(option)>=0: #Checks if the option chosen is valid, and if not sends an error message
                    return int(option)
                else:
                    print("Please enter a valid option.\n")
            else:
                print("Please enter a valid option.\n")

    def view_habits(self,habit_tracker):
        #prints a list of all habits
        print("All habits: \n\n"+habit_tracker.view_habits()+"\n")

    def view_longest_streak(self,habit_tracker):
        #prints a list of the habits with the longest streak
        print("habits with the longest streak: \n\n"+habit_tracker.view_longest_streak()+"\n")

    def view_habits_interval(self,habit_tracker):
        #prompts the user to input their chosen periodicity, and prints the data related to that chosen option
        option = int(input("\n1. Daily\n2. Weekly\nPlease enter the number of the option you would like to choose: "))

        if option ==1:
            print("Daily habits: \n\n"+habit_tracker.view_habits_interval("Daily")+"\n")

        elif option ==2:
            print("Weekly habits: \n\n"+habit_tracker.view_habits_interval("Weekly")+"\n")

        else:
            print("Please select a valid option")

    def add_habit(self,habit_tracker):
        #prompting user for habit details
        habit_name = input("Enter habit name: ")
        periodicity = int(input("1. Daily\n2. Weekly\nEnter habit interval: "))
        #send habit data to Habit_Tracker object after checking which periodicity the user has chosen, and if it is valid
        if periodicity == 1:
            habit_tracker.add_habit(habit_name,"Daily")
            print("New habit added!")
        elif periodicity == 2:
            habit_tracker.add_habit(habit_name,"Weekly")
            print("New habit added!")
        else:
            print("Please enter a valid option (1 or 2)")

    def view_specific_habit(self,habit_tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = habit_tracker.view_habit_names()
        if names is None:
            print("No habits exist\n")
        else: 
            choice = input(f"{names}\nPlease enter the number of the habit you would like to choose: ")
            #print the details of the chosen habit
            print("\nDetails of the habit: "+habit_tracker.view_specific_habit(choice)+"\n") 

 
    def update_streak(self,habit_tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = habit_tracker.view_habit_names()
        if names is None:
            print("No habits exist\n")
        else:
            choice = input(f"{names}\n\nPlease enter the number of the habit you would like the update the streak of: ")
            #updates the details of the chosen habit
            habit_tracker.update_habit(choice)
            print("Habit updated!")
            

    def delete_habit(self,habit_tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = habit_tracker.view_habit_names()
        if names is None:
            print("No habits exist\n")
        else:
            choice = input(f"{names}\n\nPlease enter the number of the habit you would like to delete: ")
            #deletes the chosen habit from the database
            habit_tracker.delete_habit(choice)
            print("Habit Deleted!")
            

class Habit_Tracker:
    def __init__(self,db_string):
        self.conn = sqlite3.connect(db_string)
        self.habits = []

    def create_table(self):
        self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS habits
        (habitID INTEGER primary key not null, name TEXT, date_created TIMESTAMP, periodicity TEXT, longest_streak INTEGER, current_streak INTEGER,last_updated TIMESTAMP)''')
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
        self.habits.append(Habit(habit_name,datetime.now(),periodicity,0,0, datetime.now()))
        #adds new habit to database
        self.conn.cursor().execute("INSERT INTO habits (name,date_created,periodicity,longest_streak,current_streak,last_update) VALUES (?,?,?,?,?,?)", (habit_name, datetime.now(), periodicity, 0, 0, datetime.now()))
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
            
        
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR,"habitdb.db")#finds the path to where the db file is stored
    habit_tracker = Habit_Tracker(db_path)
    habit_ui = Habit_UI()#creates objects of the Habit_UI and Habit_Tracker classes
    habit_tracker.load_habits()#calls for the method to load the habits in the database into a list

    while True: #continuously loops to display the menu when the user is finished with an action
        habit_ui.print_menu()
        option = habit_ui.get_option()

        if option ==1:
            habit_ui.view_habits(habit_tracker)

        elif option == 2:
            habit_ui.add_habit(habit_tracker)

        elif option ==3:
            habit_ui.view_longest_streak(habit_tracker)
        
        elif option ==4:
            habit_ui.view_specific_habit(habit_tracker)

        elif option ==5:
            habit_ui.view_habits_interval(habit_tracker)

        elif option ==6:
            habit_ui.update_streak(habit_tracker)
        
        elif option ==7:
            habit_ui.delete_habit(habit_tracker)

        elif option ==0:
            print("Exiting program...")
            break

        else:
            print("Please select a valid option")
