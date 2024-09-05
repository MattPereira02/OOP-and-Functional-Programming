**Habit Tracker Application**

**Overview**

This is a simple Habit Tracking application written in Python 3.11.7. The application uses an SQLite3 database to store habit data. The data stored for each habit includes:

    Name: Name of the habit
    Date Created: Date when the habit was created
    Periodicity: Either daily or weekly
    Current Streak: Number of days or weeks the habit has been consistently practiced
    Longest Streak: Longest streak of consistent practice for the habit

**Features**

The application provides the following functions to manage and track habits:

    Create Habit: Add a new habit with all the required details.
    Delete Habit: Remove a habit from the database.
    Display All Habits: View a list of all habits along with their details.
    Display Habits with Longest Streak: Show habits with the longest streaks.
    Search for Specific Habit: Search and display details of a specific habit.
    Display Habits of Specific Periodicity: View habits based on their periodicity (daily or weekly).
    Update Habit Streak: Update the streak of a specific habit.
    Delete Habit: Delete a habit from the database.

**Requirements**

    Python 3.11.7
    SQLite3

**Installation and Setup**

  1. Clone the Repository:

    git clone https://github.com/MattPereira02/OOP-and-Functional-Programming/habit-tracker.git

  2. Navigate to the Directory:

    cd habit-tracker

  3. Install Required Packages:
   
    No external packages are required as SQLite3 and Python's standard libraries are used.

**Usage**

  Run the Application:

    python habit_tracker.py

Follow On-screen Instructions:

    Choose options from the menu to perform various actions like creating, deleting, or updating habits.
    Enter data as prompted to interact with the application.

**Testing**

  Run test script:

    pytest .
    

**Database Schema**

The SQLite3 database has the following schema:
      
      CREATE TABLE habits (
        habitID INTEGER primary key not null, name TEXT, date_created TIMESTAMP, periodicity TEXT, longest_streak INTEGER, current_streak INTEGER, last_updated TIMESTAMP
        );

**License**

    This project is licensed under the MIT License. See the LICENSE file for details.

**Maintained by Matthew Pereira**
