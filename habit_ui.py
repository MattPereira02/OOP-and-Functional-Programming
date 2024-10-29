import os.path
from habit_tracker import Habit_Tracker

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

    def view_habits(self,tracker):
        #prints a list of all habits
        print("All habits: \n\n"+tracker.view_habits()+"\n")

    def view_longest_streak(self,tracker):
        #prints a list of the habits with the longest streak
        print("habits with the longest streak: \n\n"+tracker.view_longest_streak()+"\n")

    def view_habits_interval(self,tracker):
        #prompts the user to input their chosen periodicity, and prints the data related to that chosen option
        option = int(input("\n1. Daily\n2. Weekly\nPlease enter the number of the option you would like to choose: "))

        if option ==1:
            print("Daily habits: \n\n"+tracker.view_habits_interval("Daily")+"\n")

        elif option ==2:
            print("Weekly habits: \n\n"+tracker.view_habits_interval("Weekly")+"\n")

        else:
            print("Please select a valid option")

    def add_habit(self,tracker):
        #prompting user for habit details
        habit_name = input("Enter habit name: ")
        periodicity = int(input("1. Daily\n2. Weekly\nEnter habit interval: "))
        #send habit data to Habit_Tracker object after checking which periodicity the user has chosen, and if it is valid
        if periodicity == 1:
            tracker.add_habit(habit_name,"Daily")
            print("New habit added!")
        elif periodicity == 2:
            tracker.add_habit(habit_name,"Weekly")
            print("New habit added!")
        else:
            print("Please enter a valid option (1 or 2)")

    def view_specific_habit(self,tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = tracker.view_habit_names()
        if names is None:
            print("No habits found\n")
        else: 
            choice = input(f"{names}\nPlease enter the number of the habit you would like to choose: ")
            #print the details of the chosen habit
            print("\nDetails of the habit: "+tracker.view_specific_habit(choice)+"\n") 

 
    def update_streak(self,tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = tracker.view_habit_names()
        if names is None:
            print("No habits found\n")
        else:
            choice = input(f"{names}\n\nPlease enter the number of the habit you would like the update the streak of: ")
            #updates the details of the chosen habit
            tracker.update_habit(choice)
            print("Habit updated!")
            

    def delete_habit(self,tracker):
        #displays the names of all habits to the user, and then prompts them to input the number of the habit they would like to view
        names = tracker.view_habit_names()
        if names is None:
            print("No habits found\n")
        else:
            choice = input(f"{names}\n\nPlease enter the number of the habit you would like to delete: ")
            #deletes the chosen habit from the database
            tracker.delete_habit(choice)
            print("Habit Deleted!")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR,"habitdb.db")#finds the path to where the db file is stored
    tracker = Habit_Tracker(db_path)
    habit_ui = Habit_UI()#creates objects of the Habit_UI and Habit_Tracker classes
    tracker.load_habits()#calls for the method to load the habits in the database into a list

    while True: #continuously loops to display the menu when the user is finished with an action
        habit_ui.print_menu()
        option = habit_ui.get_option()

        if option ==1:
            habit_ui.view_habits(tracker)

        elif option == 2:
            habit_ui.add_habit(tracker)

        elif option ==3:
            habit_ui.view_longest_streak(tracker)
        
        elif option ==4:
            habit_ui.view_specific_habit(tracker)

        elif option ==5:
            habit_ui.view_habits_interval(tracker)

        elif option ==6:
            habit_ui.update_streak(tracker)
        
        elif option ==7:
            habit_ui.delete_habit(tracker)

        elif option ==0:
            print("Exiting program...")
            break

        else:
            print("Please select a valid option")
