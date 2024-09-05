import pytest
import habit_tracker
import os
from datetime import datetime, timedelta
from unittest.mock import patch

class TestHabit:
    def setup_db(self):
        #Creates test database
        habit_tracker.init('test_db')
        habit_tracker.create_table()
        yield
        #Teardown test database
        if os.path.exists('test_db'):
            os.remove('test_db')
        
    def test_add_habit(setup_db):
        # Tests that the 'add habit' function
        habit_tracker.add_habit('Exercise', 'Daily')
        habit = habit_tracker.view_specific_habit(1)
        assert habit['name'] == 'Exercise'
        assert habit['periodicity'] == 'Daily'

    def test_delete_habit(setup_db):
        #Tests the 'delete habit' function
        habit_tracker.add_habit('Exercise', 'Daily')
        habit_tracker.delete_habit(1)
        habit = habit_tracker.view_specific_habit(1)
        assert habit is None

    def test_view_habits(setup_db):
        #Tests displaying all habits
        habit_tracker.add_habit('Exercise', 'Daily')
        habit_tracker.add_habit('Clean Shower', 'Weekly')
        habits = habit_tracker.view_habits()
        assert habits == f"Habit: Exercise, Created: {datetime.strftime(datetime.now, "%d-%m-%Y")}, Period: Daily, Current streak: 0, Longest streak: 0 \n Habit: Clean Shower, Created: {datetime.strftime(datetime.now, "%d-%m-%Y")}, Period: Weekly, Current streak: 0, Longest streak: 0"

    def test_update_streak(setup_db):
        #Tests updating streak function
         habit_tracker.add_habit('Exercise','Daily')
         habit_tracker.update_habit(1)
         habit = habit_tracker.view_specific_habit(1)
         assert habit['current_streak'] == 1
         assert habit['longest_streak'] == 1

    @patch('habit_tracker.datetime')
    def test_update_streak_multiple(mock_datetime,setup_db):
        #Tests updating streak function over multiple days
        habit_tracker.add_habit('Exercise', 'Daily')
        habit_tracker.update_habit(1)
        current_date = datetime.now() + timedelta(days=1)
        mock_datetime.now.return_value.date.return_value = current_date
        habit_tracker.update_habit(1)
        habit = habit_tracker.view_specific_habit(1)
        assert habit['current_streak'] == 2
        assert habit['longest_streak'] == 2
    
    def test_view_longest_streak(setup_db):
        #Tests the view habits with longest streak function
        habit_tracker.add_habit('Exercise', 'Daily')
        habit_tracker.add_habit('Clean Shower', 'Weekly')
        habit_tracker.add_habit('Study', 'Daily')
        habit_tracker.update_habit(1)
        habit_tracker.update_habit(3)
        habit = habit_tracker.view_longest_streak()
        newline_count = habit.count('\n')
        assert newline_count == 1
        assert 'Exercise' in habit
        assert 'Study' in habit

    def test_multiple_dates(self):
        #Checks if current and longest streak compute correctly with multiple consecutive dates
        self.habit1.update_streak("14-03-2024 09:23.0")
        self.habit1.update_streak("15-03-2024 09:33.0")
        self.habit1.update_streak("16-03-2024 09:25.0")
        assert self.habit1.current_streak == 3

        #Checking that the current and longest streak compute correctly with non-consecutive dates
        self.habit1.update_streak("18-03-2024 10:12.0")
        assert self.habit1.current_streak == 0
        assert self.habit1.longest_streak == 3

#Run the tests
pytest.main()