import pandas as pd
from datetime import datetime
import time

PANDA_NAME = "PANDA"

def panda_speak(msg):
    print(f"\n🐼 {PANDA_NAME}: {msg}")

# ---- Food Database (25 foods) ----
foods = {
    'FoodName': [
        'Chicken Breast', 'White Rice', 'Broccoli', 'Peanut Butter', 'Banana',
        'Apple', 'Egg', 'Milk', 'Oats', 'Paneer',
        'Chapati', 'Dal', 'Almonds', 'Yogurt', 'Potato',
        'Tofu', 'Cheese', 'Fish', 'Bread', 'Pasta',
        'Olive Oil', 'Cucumber', 'Tomato', 'Orange', 'Honey'
    ],
    'StandardUnit': [
        '100g', 'serving', 'cup', 'tbsp', 'unit',
        'unit', 'unit', 'cup', 'cup', '100g',
        'piece', 'cup', '10 pieces', 'cup', '100g',
        '100g', 'slice', '100g', 'slice', 'cup',
        'tbsp', 'cup', 'unit', 'unit', 'tbsp'
    ],
    'StandardAmount': [
        100, 1, 91, 32, 1,
        1, 1, 240, 81, 100,
        1, 100, 10, 245, 100,
        100, 1, 100, 1, 100,
        14, 100, 1, 1, 21
    ],
    'Calories': [
        165, 205, 31, 188, 105,
        95, 78, 150, 150, 265,
        120, 130, 70, 100, 77,
        76, 113, 206, 80, 160,
        120, 16, 22, 62, 64
    ],
    'Protein': [
        31, 4.3, 2.6, 8, 1.3,
        0.5, 6.3, 8, 5, 18,
        3, 9, 3, 6, 2,
        8, 7, 22, 3, 5,
        0, 0.7, 1, 1.2, 0
    ],
    'Fat': [
        3.6, 0.4, 0.3, 16, 0.3,
        0.3, 5.3, 8, 3, 20,
        3.6, 1.2, 6, 3, 0.1,
        4.8, 9, 12, 1, 1,
        14, 0.1, 0.2, 0.2, 0
    ],
    'Carbs': [
        0, 45, 6, 7, 27,
        25, 0.6, 12, 27, 4,
        20, 18, 2, 12, 17,
        2, 0.4, 0, 14, 31,
        0, 3.6, 5, 15, 17
    ]
}

db_foods = pd.DataFrame(foods)
db_foods.set_index('FoodName', inplace=True)

# ---- Logs and Targets ----
log_daily = pd.DataFrame(columns=['Date', 'Time', 'Food', 'Amount', 'Unit', 'Calories', 'Protein', 'Fat', 'Carbs'])
targets = {'Calories': 2000, 'Protein': 150, 'Fat': 70, 'Carbs': 250}


def log_meal():
    global log_daily
    panda_speak("Let's add what you just ate!")

    print("\nHere’s what I know:")
    for i, food in enumerate(db_foods.index):
        print(f"{i+1}. {food} ({db_foods.loc[food, 'StandardUnit']})")

    try:
        choice = int(input("Enter number: ")) - 1
        food_name = db_foods.index[choice]
    except:
        panda_speak("Oops, that's not valid.")
        return

    try:
        amount = float(input(f"How much {food_name} did you eat? "))
    except:
        panda_speak("Please enter a number next time!")
        return

    row = db_foods.loc[food_name]
    factor = amount / row['StandardAmount']

    cal = row['Calories'] * factor
    pro = row['Protein'] * factor
    fat = row['Fat'] * factor
    carb = row['Carbs'] * factor

    entry = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Time': datetime.now().strftime("%H:%M:%S"),
        'Food': food_name,
        'Amount': amount,
        'Unit': row['StandardUnit'],
        'Calories': cal,
        'Protein': pro,
        'Fat': fat,
        'Carbs': carb
    }

    log_daily = pd.concat([log_daily, pd.DataFrame([entry])], ignore_index=True)
    panda_speak(f"Added {round(cal)} kcal from {food_name}! Nice job.")


def view_summary():
    if log_daily.empty:
        panda_speak("No meals logged yet. Let’s start eating!")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    today_log = log_daily[log_daily['Date'] == today]

    if today_log.empty:
        panda_speak("No meals today yet!")
        return

    total = today_log[['Calories', 'Protein', 'Fat', 'Carbs']].sum()
    print("\n----------------------------")
    print(f"     DAILY SUMMARY ({today})")
    print("----------------------------")
    print(total)

    print("\nYour Targets:")
    for k, v in targets.items():
        print(f"{k}: {v}")

    print("\nRemaining:")
    for k in targets:
        rem = targets[k] - total[k]
        print(f"{k}: {rem:.1f}")

    panda_speak("Here’s how you’re doing today! Keep going strong 💪")


def view_weekly_summary():
    if log_daily.empty:
        panda_speak("No meals logged yet!")
        return

    # Group by date and sum
    week_data = log_daily.groupby('Date')[['Calories', 'Protein', 'Fat', 'Carbs']].sum()

    print("\n===============================")
    print("        WEEKLY SUMMARY")
    print("===============================")
    print(week_data)

    total_week = week_data.sum()
    avg_week = week_data.mean()

    print("\n---- Weekly Totals ----")
    print(total_week)

    print("\n---- Daily Averages ----")
    print(avg_week)

    panda_speak("That’s your performance for the week! 🐾")


def set_targets():
    panda_speak("Let’s set your nutrition goals!")
    for k, v in targets.items():
        print(f"{k}: {v}")

    try:
        choice = input("Change one (Calories/Protein/Fat/Carbs or all): ").title()
        if choice == "All":
            for k in targets:
                targets[k] = float(input(f"New {k}: "))
        elif choice in targets:
            targets[choice] = float(input(f"New {choice}: "))
        else:
            panda_speak("Not a valid option.")
    except:
        panda_speak("Something went wrong. Try again!")

    panda_speak("Targets updated!")


def main():
    panda_speak("Hey there! I'm PANDA, your food tracking buddy 🐾")

    run = True
    while run:
        print("\n========== MENU ==========")
        print("1. Log Meal")
        print("2. View Today Summary")
        print("3. View Weekly Summary")
        print("4. Set Targets")
        print("5. Exit")
        print("==========================")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            log_meal()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            view_weekly_summary()
        elif choice == '4':
            set_targets()
        elif choice == '5':
            panda_speak("Goodbye! Remember to eat well 😊")
            run = False
        else:
            panda_speak("Please pick between 1 and 5.")

        time.sleep(0.5)


if __name__ == "__main__":
    main()