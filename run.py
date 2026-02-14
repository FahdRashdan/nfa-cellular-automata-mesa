# Mesa visualization components
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer

# UI slider component for interactive parameters
from mesa.visualization.UserParam import Slider

# Import the model we want to visualize
from model import NFACAModel


# 🎨 AGENT VISUALIZATION FUNCTION
# This function tells Mesa HOW to draw each agent on the grid
def agent_portrayal(agent):

    # Base visual properties shared by all agents
    portrayal = {
        "Shape": "rect",      # Draw agent as a square cell
        "w": 1,               # Full cell width
        "h": 1,               # Full cell height
        "Filled": "true",     # Fill the shape with color
        "Layer": 0,           # Rendering layer
    }

    # Color depends on the agent's current NFA state
    if agent.state == "Alive":
        portrayal["Color"] = "green"     # Healthy / active
    elif agent.state == "Dying":
        portrayal["Color"] = "red"       # Decaying
    elif agent.state == "Stable":
        portrayal["Color"] = "purple"    # Balanced / stable
    else:  # Chaotic
        portrayal["Color"] = "gray"      # Chaotic / noisy

    # Return the visual representation of the agent
    return portrayal


# 🧱 FIXED GRID VISUALIZATION (20 × 20)
grid = CanvasGrid(
    agent_portrayal,  # Function used to draw agents
    20,               # Grid width (cells)
    20,               # Grid height (cells)
    600,              # Canvas width in pixels
    600               # Canvas height in pixels
)

# 📈 REAL-TIME CHART MODULE
# Displays how many agents are in each state over time
chart = ChartModule(
    [
        {"Label": "Alive", "Color": "green"},
        {"Label": "Dying", "Color": "red"},
        {"Label": "Stable", "Color": "purple"},
        {"Label": "Chaotic", "Color": "gray"},
    ],
    # Uses the DataCollector defined in the model
    data_collector_name="datacollector"
)

# 🎛 INTERACTIVE PARAMETERS (BONUS FEATURES)
# Sliders allow the user to modify model behavior at runtime
model_params = {

    # Controls initial probability of Alive cells
    "initial_alive": Slider(
        "Initial Alive Ratio",  # Label shown in UI
        0.3,                    # Default value
        0.0,                    # Minimum
        1.0,                    # Maximum
        0.05                    # Step size
    ),

    # Controls nondeterministic branching probability in the NFA
    "branch_prob": Slider(
        "Branching Probability",
        0.5,
        0.0,
        1.0,
        0.05
    ),

    # Controls how strongly Chaotic transitions are favored
    "chaos_bias": Slider(
        "Chaos Bias (Rewire NFA)",
        0.2,
        0.0,
        1.0,
        0.05
    ),

    # Enables or disables the Chaotic state completely
    # 0 → Chaotic allowed
    # 1 → Chaotic disabled
    "disable_chaotic": Slider(
        "Disable Chaotic State",
        0,
        0,
        1,
        1
    ),
}

# 🚀 CREATE AND RUN THE SERVER
server = ModularServer(
    NFACAModel,                     # Model class
    [grid, chart],                  # Visualization modules
    "NFA Cellular Automata (Interactive)",  # Page title
    model_params                    # User-controlled parameters
)

# Port where the web app will run
server.port = 8521

# Start the visualization server
server.launch()
