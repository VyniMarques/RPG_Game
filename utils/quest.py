import random

class Mission:
    def __init__(self, name, description, objective_count, objective_type):
        self.name = name
        self.description = description
        self.objective_count = objective_count  # Objective amount (ex: 5 inimigos)
        self.current_count = 0
        self.objective_type = objective_type  # ex: "kill_enemy"
        self.completed = False

    def update_progress(self):
        if not self.completed:
            self.current_count += 1
            if self.current_count >= self.objective_count:
                self.completed = True
                print(f"Quest '{self.name}' completed!")

    def reset(self):
        self.current_count = 0
        self.completed = False


def checkQuest(enemy, missions):
    if not enemy.alive and not getattr(enemy, "counted_for_mission", False):
        enemy.counted_for_mission = True
        for mission in missions:
            if mission.objective_type == "kill_enemy":
                mission.update_progress()

def showQuest(possible_missions, missions):
    if len(possible_missions) != 0:
        aux = random.randint(0, len(possible_missions) - 1)
        aux_mission = possible_missions[aux]
        possible_missions.remove(aux_mission)
        missions.append(aux_mission)


def completeQuest(possible_missions, missions):
    completed_missions = [mission for mission in missions if mission.completed]
    
    for mission in completed_missions:
        missions.remove(mission)  
        mission.reset()  
        possible_missions.append(mission)  
    