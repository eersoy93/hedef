import json
import os
import sys


EXIT_SUCCESS = 0
EXIT_FAILURE = 1

FILENAME = "goals.json"


class Hedef:
    next_goal_id = 1
    goals = []

    def __init__(self, goal_id, goal_name, goal_completed=False):
        self.goal_id = goal_id
        self.goal_name = goal_name
        self.goal_completed = goal_completed

    def __str__(self):
        status = "X" if self.goal_completed else "."
        return f"[{status}] {self.goal_id} {self.goal_name}"


def load_goals():
    if os.stat(FILENAME).st_size == 0:
        Hedef.goals = []
        Hedef.next_goal_id = 1
    else:
        try:
            with open(FILENAME, "r") as file:
                goals_list = json.loads(file.read())

                for goal in goals_list:
                    Hedef.goals.append(Hedef(goal["goal_id"], goal["goal_name"], goal["goal_completed"]))

                if Hedef.goals:
                    Hedef.next_goal_id = max([goal.goal_id for goal in Hedef.goals]) + 1
                else:
                    Hedef.next_goal_id = 1
        except FileNotFoundError:
            Hedef.goals = []
            Hedef.next_goal_id = 1

    return Hedef.goals


def save_goals():
    with open(FILENAME, "w") as file:
        json.dump([{"goal_id": goal.goal_id, "goal_name": goal.goal_name, "goal_completed": goal.goal_completed} for goal in Hedef.goals], file, indent=4)

    try:
        Hedef.next_goal_id = max([goal.goal_id for goal in Hedef.goals]) + 1
    except ValueError:
        Hedef.next_goal_id = 1


def add_goal(goal_name):
    Hedef.goals = load_goals()

    for goal in Hedef.goals:
        if goal.goal_name == goal_name:
            print(f"The goal already exists: {goal}")
            sys.exit(EXIT_FAILURE)

    goal = Hedef(Hedef.next_goal_id, goal_name, False)

    Hedef.goals.append(goal)

    save_goals()

    print(f"The goal has been appended: {goal}")


def list_goals():
    Hedef.goals = load_goals()

    for goal in Hedef.goals:
        print(goal)


def complete_goal(i):
    Hedef.goals = load_goals()

    i = int(i)

    for goal in Hedef.goals:
        if goal.goal_id == i:
            if goal.goal_completed:
                print(f"The goal is already completed: {goal}")
                sys.exit(EXIT_FAILURE)
            goal.goal_completed = True
            break
    else:
        print(f"Invalid goal id number to complete: {i}")
        sys.exit(EXIT_FAILURE)

    save_goals()

    print(f"The goal has been completed: {goal}")


def delete_goal(i):
    Hedef.goals = load_goals()

    i = int(i)

    for goal in Hedef.goals:
        if goal.goal_id == i:
            Hedef.goals.remove(goal)
            break
    else:
        print(f"Invalid goal id number to delete: {i}")
        sys.exit(EXIT_FAILURE)

    save_goals()

    print(f"The goal has been removed: {goal}")


def main(args):
    if len(args) == 2 or len(args) == 3:
        command = args[1]

        if command == "add":
            if len(args) != 3:
                print("Invalid argument count! Usage: python/python3 hedef.py add <goal_name>")
                return EXIT_FAILURE

            add_goal(args[2])
        elif command == "list":
            if len(args) != 2:
                print("Invalid argument count! Usage: python/python3 hedef.py list")
                return EXIT_FAILURE

            list_goals()
        elif command == "complete":
            if len(args) != 3:
                print("Invalid argument count! Usage: python/python3 hedef.py complete <goal_id>")
                return EXIT_FAILURE

            complete_goal(args[2])
        elif command == "delete":
            if len(args) != 3:
                print("Invalid argument count! Usage: python/python3 hedef.py delete <goal_id>")
                return EXIT_FAILURE

            delete_goal(args[2])
        else:
            print("Invalid command! Usage: python/python3 hedef.py <add|list|complete|delete>")
            return EXIT_FAILURE
    else:
            print("Invalid argument count! Usage: python/python3 hedef.py <add|list|complete|delete>")
            return EXIT_FAILURE

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main(sys.argv))
