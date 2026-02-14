# Standard Python library for randomness
import random

# Mesa base Agent class
from mesa import Agent


# Each agent represents ONE CELL in the cellular automaton
# and ONE STATE MACHINE in the NFA
class NFACellAgent(Agent):

    def __init__(self, unique_id, model, state):
        # Initialize Mesa Agent with unique ID and reference to the model
        super().__init__(unique_id, model)

        # Current NFA state of the agent
        self.state = state

        # Next state (used for simultaneous updates)
        self.next_state = state

    # This method computes the agent's next state
    # (does NOT update it immediately)
    def step(self):

        # Get neighboring agents from the grid
        # moore=True → 8-direction neighbors
        # include_center=False → do not include itself
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )

        # Count how many neighbors are in the "Alive" state
        alive_neighbors = sum(1 for n in neighbors if n.state == "Alive")

        # Convert number of alive neighbors into NFA input symbol
        # This symbol acts as the input alphabet of the NFA
        if alive_neighbors <= 2:
            input_symbol = "L"   # Low density
        elif alive_neighbors <= 4:
            input_symbol = "M"   # Medium density
        else:
            input_symbol = "H"   # High density

        # 🔁 Get dynamically rewired NFA transitions from the model
        transitions = self.model.get_transitions()

        # Get list of possible next states from the NFA
        # Based on (current_state, input_symbol)
        possible_states = transitions[(self.state, input_symbol)]

        # 🎯 Nondeterministic transition choice
        # If only one possible state → deterministic
        if len(possible_states) == 1:
            self.next_state = possible_states[0]

        # If multiple possible states → probabilistic branching
        else:
            # branch_prob controls likelihood of choosing the first state
            weights = [self.model.branch_prob, 1 - self.model.branch_prob]

            # Randomly choose next state based on weights
            self.next_state = random.choices(
                possible_states,
                weights=weights,
                k=1
            )[0]

        # 🚫 INTERACTIVE STATE REMOVAL
        # If chaotic behavior is disabled and the chosen state is "Chaotic"
        # force the agent into a safe fallback state
        if self.model.disable_chaotic == 1 and self.next_state == "Chaotic":
            self.next_state = "Stable"

    # This method applies the state update
    # Called AFTER all agents finish step()
    def advance(self):
        self.state = self.next_state
