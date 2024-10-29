from habit_tracker import Habit_Tracker
import os
from datetime import datetime
import pytest

class TestHabit:
        
    @pytest.fixture
    def setup_db(self):
        #Creates test database
        self.tracker = Habit_Tracker('test_db.db')
        self.tracker.create_table()
        yield self.tracker
        #Teardown test database
        self.tracker.conn.close()
        if os.path.exists('test_db.db'):
            os.remove('test_db.db')

    @staticmethod
    def run_tests():
        print("Running all unit tests...")
        pytest.main([__file__])
        print("Unit tests completed.")

   
    def test_add_habit(self,setup_db):
        #Tests that the 'add_habit' function works correctly
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        assert self.tracker.habits[0].get_name() == 'Exercise'
        assert self.tracker.habits[0].get_periodicity() == 'Daily'

    def test_delete_habit(self,setup_db):
        #Tests the 'delete habit' function
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.delete_habit(1)
        assert len(self.tracker.habits) == 0

    def test_view_habits(self,setup_db):
        #Tests displaying all habits
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.add_habit('Clean Shower', 'Weekly')
        habits = self.tracker.view_habits()
        assert 'Habit: Exercise' in habits
        assert 'Habit: Clean Shower' in habits

    def test_habits_interval(self,setup_db):
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.add_habit('Clean Shower', 'Weekly')
        habits = self.tracker.view_habits_interval('Daily')
        assert 'Exercise' in habits
        assert 'Clean Shower' not in habits

    def test_view_specific_habit(self,setup_db):
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.add_habit('Clean Shower', 'Weekly')
        habits = self.tracker.view_specific_habit(2)
        assert 'Clean Shower' in habits

    def test_update_streak(self,setup_db):
        #Tests updating streak function
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.update_habit(1)
        assert self.tracker.habits[0].current_streak == 1
        assert self.tracker.habits[0].longest_streak == 1
    
    def test_view_longest_streak(self,setup_db):
        #Tests the view habits with longest streak function
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.add_habit('Clean Shower', 'Weekly')
        self.tracker.add_habit('Study', 'Daily')
        self.tracker.update_habit(1)
        self.tracker.update_habit(3)
        habit = self.tracker.view_longest_streak()
        assert 'Exercise' in habit
        assert 'Study' in habit
        assert 'Clean Shower' not in habit

    def test_multiple_dates(self,setup_db):
        #Checks if current and longest streak compute correctly with multiple consecutive dates
        self.tracker = setup_db
        self.tracker.add_habit('Exercise', 'Daily')
        self.tracker.habits[0].update_streak(datetime(2024,3,14))
        self.tracker.habits[0].update_streak(datetime(2024,3,15))
        self.tracker.habits[0].update_streak(datetime(2024,3,16))
        assert self.tracker.habits[0].current_streak == 3

        #Checking that the current and longest streak compute correctly with non-consecutive dates
        self.tracker.habits[0].update_streak(datetime(2024,3,18))
        assert self.tracker.habits[0].current_streak == 1
        assert self.tracker.habits[0].longest_streak == 3

if __name__ == "__main__":
    TestHabit.run_tests()
