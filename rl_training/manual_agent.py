from rl_training.game_environment import GameEnv
from gameplay.enums import Action, State, Occupation


class ManualAgent:
    def __init__(self, env: GameEnv, doctor_bound, engineer_bound, injured_bound: int = 0, scram_bound: int = 9):
        """
        Fixed strategy
            SAVE all HEALTHY
            SQUISH all ZOMBIE and CORPSE
            SAVE / SQUISH injured

        injured_bound is the max capacity where the agent will save injured
            if capacity <= injured_bound:
                SAVE injured people
            else if capacity > injured_bound:
                SQUISH injured people

        scram_bound is the minimum capacity where the agent will scram early
            only scrams early if faced with an injured person
            if capacity >= scram_bound:

        """
        self.env = env
        self.injured_bound = injured_bound
        self.scram_bound = scram_bound
        self.doctor_bound = doctor_bound
        self.engineer_bound = engineer_bound

        assert 0 <= self.scram_bound <= 10
        assert 0 <= self.injured_bound <= 10

    def get_action(self, obs) -> int:
        state = self.env.humanoid_number_to_state[obs['humanoid_status']]
        occupation = self.env.number_to_occupation[obs['humanoid_occupation']]
        capacity = obs['capacity']
        cures = obs['cures']

        # if injured and have cure - consider person healthy
        if state == State.INJURED.value and cures > 0:
            state = State.HEALTHY.value

        action = None

        # always squish zombies and corpses
        if state == State.CORPSE.value or state == State.ZOMBIE.value:
            action = Action.SQUISH
        # always save healthy
        elif state == State.HEALTHY.value:
            action = Action.SAVE
        # injured depends on bounds
        elif state == State.INJURED.value:
            bound = self.injured_bound
            if occupation == Occupation.DOCTOR.value:
                bound = self.doctor_bound
            elif occupation == Occupation.ENGINEER.value:
                bound = self.engineer_bound

            if capacity <= bound:
                action = Action.SAVE
            elif capacity >= self.scram_bound:
                action = Action.SCRAM
            else:
                action = Action.SQUISH

        # perform action if legal
        if self.env.is_legal(self.env.action_str_to_number[action.value]):
            return self.env.action_str_to_number[action.value]
        # scram if not
        else:
            return self.env.action_str_to_number[Action.SCRAM.value]
