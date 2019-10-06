from ToPCLI.Todoist import Todoist

def main():
    todoist = Todoist()
    projects = todoist.get_state("projects")
    print(projects)
    tasks = todoist.get_state("items")
    print(tasks)
    todoist.add("projects", "Test")
