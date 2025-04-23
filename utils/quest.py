import random

class Mission:
    def __init__(self, name, description, objective_count, objective_type):
        self.name = name
        self.description = description
        self.objective_count = objective_count
        self.current_count = 0
        self.objective_type = objective_type
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


class MissionManager:
    def __init__(self):
        self.possible_missions = [
            Mission("Hunter", "Kill 2 enemies.", 2, "kill_enemy"),
            Mission("Monster Hunter", "Kill 2 enemies.", 2, "kill_enemy"),
            Mission("Monster Killer", "Kill 10 enemies.", 10, "kill_enemy"),
            Mission("Monster Assasin", "Kill 15 enemies.", 15, "kill_enemy"),
        ]
        self.missions = []

    def check_quests(self, enemy):
        if not enemy.alive and not getattr(enemy, "counted_for_mission", False):
            enemy.counted_for_mission = True
            for mission in self.missions:
                if mission.objective_type == "kill_enemy":
                    mission.update_progress()

    def get_new_quest(self):
        if len(self.missions) < 3 and self.possible_missions:
            new_quest = random.choice(self.possible_missions)
            self.possible_missions.remove(new_quest)
            self.missions.append(new_quest)

    def complete_quest(self):
        
        completed_missions = [m for m in self.missions if m.completed]
        
        if completed_missions:
            print("Missões completas:")
            for m in completed_missions:
                print(f"  {m.name}")
            
            for m in completed_missions:
                self.missions.remove(m)
                m.reset()
                self.possible_missions.append(m)
