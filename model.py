# Standard Python library for randomness
import random

# Mesa core model class
from mesa import Model

# Scheduler where all agents update at the same time
# (important for Cellular Automata behavior)
from mesa.time import SimultaneousActivation

# Grid that allows multiple agents per cell
from mesa.space import MultiGrid

# Tool to collect data during simulation (for plots/analysis)
from mesa.datacollection import DataCollector

# Our custom agent class (each grid cell is an NFA agent)
from agent import NFACellAgent


# Main model class combining:
# - NFA (state transitions)
# - Cellular Automaton (grid-based agents)
class NFACAModel(Model):

    def __init__(
        self,
        initial_alive,     # Probability that a cell starts in "Alive" state
        branch_prob,       # Probability used for nondeterministic branching
        chaos_bias,        # Controls preference for "Chaotic" transitions
        disable_chaotic    # If True, removes "Chaotic" state entirely
    ):
        # Initialize Mesa base Model
        super().__init__()

        # 🔒 FIXED GRID SIZE
        self.width = 20
        self.height = 20
        # 20 × 20 grid → 400 agents total
        # (UI note: grid is rendered as ~600 pixels)

        # Store parameters so agents can access them
        self.branch_prob = branch_prob
        self.chaos_bias = chaos_bias
        self.disable_chaotic = disable_chaotic

        # Create a toroidal grid (edges wrap around)
        self.grid = MultiGrid(self.width, self.height, torus=True)

        # Scheduler where all agents act simultaneously
        self.schedule = SimultaneousActivation(self)

        # 🔁 BASE NFA TRANSITION RULES
        # Key  : (current_state, neighborhood_density)
        # Value: list of possible next states (NFA branching)
        self.BASE_TRANSITIONS = {

            # Alive state transitions
            ("Alive", "L"): ["Alive", "Stable"],
            ("Alive", "M"): ["Dying", "Chaotic"],
            ("Alive", "H"): ["Chaotic", "Dying"],

            # Dying state transitions
            ("Dying", "L"): ["Stable", "Alive"],
            ("Dying", "M"): ["Chaotic", "Alive"],
            ("Dying", "H"): ["Chaotic", "Dying"],

            # Stable state transitions
            ("Stable", "L"): ["Alive", "Stable"],
            ("Stable", "M"): ["Dying", "Stable"],
            ("Stable", "H"): ["Chaotic", "Stable"],

            # Chaotic state transitions
            ("Chaotic", "L"): ["Stable", "Alive"],
            ("Chaotic", "M"): ["Alive", "Dying"],
            ("Chaotic", "H"): ["Chaotic", "Dying"],
        }

        # 🌱 INITIALIZE GRID WITH AGENTS
        for x in range(self.width):
            for y in range(self.height):

                # Randomly assign initial state
                # Alive with probability = initial_alive
                # Otherwise Stable
                state = "Alive" if random.random() < initial_alive else "Stable"

                # Create an NFA cell agent
                agent = NFACellAgent((x, y), self, state)

                # Place agent on the grid
                self.grid.place_agent(agent, (x, y))

                # Add agent to the scheduler
                self.schedule.add(agent)

        # 📊 DATA COLLECTION
        # Counts how many agents are in each state at every step
        self.datacollector = DataCollector(
            model_reporters={
                "Alive": lambda m: self.count_state("Alive"),
                "Dying": lambda m: self.count_state("Dying"),
                "Stable": lambda m: self.count_state("Stable"),
                "Chaotic": lambda m: self.count_state("Chaotic"),
            }
        )

    # 🔁 INTERACTIVE NFA REWIRING (BONUS FEATURE)
    # Dynamically modifies NFA transitions based on chaos parameters
    def get_transitions(self):
        transitions = {}

        # Loop over base transition rules
        for key, states in self.BASE_TRANSITIONS.items():

            # Copy list to avoid changing original rules
            reordered = states.copy()

            # If chaos bias is high → prefer Chaotic transitions
            if self.chaos_bias > 0.7:
                # Moves "Chaotic" to the front of the list
                reordered = sorted(reordered, key=lambda s: s != "Chaotic")

            # If chaos bias is low → avoid Chaotic transitions
            elif self.chaos_bias < 0.3:
                # Pushes "Chaotic" to the end
                reordered = sorted(reordered, key=lambda s: s == "Chaotic")

            # If chaotic behavior is disabled completely
            if self.disable_chaotic:
                # Remove "Chaotic" from transition options
                reordered = [s for s in reordered if s != "Chaotic"]

                # Safety fallback: NFA must have at least one transition
                if not reordered:
                    reordered = ["Stable"]

            # Save modified transitions
            transitions[key] = reordered

        # Return dynamically rewired NFA transition table
        return transitions

    # 🔁 One simulation step
    def step(self):
        # Collect statistics for this step
        self.datacollector.collect(self)

        # Let all agents compute & apply their next state simultaneously
        self.schedule.step()

    # 📊 Helper function to count agents in a given state
    def count_state(self, state):
        # Counts agents whose current state matches the input
        return sum(1 for a in self.schedule.agents if a.state == state)
