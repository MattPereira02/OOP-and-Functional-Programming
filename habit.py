from datetime import datetime

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
