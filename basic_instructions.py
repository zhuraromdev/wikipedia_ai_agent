import json


class Task:
    def __init__(self, description, steps):
        self.description = description
        self.steps = steps


class Step:
    def __init__(self, action, target=None, value=None):
        self.action = action
        self.target = target
        self.value = value


def parse_instruction(instruction):
    # Dummy parser for demonstration purposes
    # In a real scenario, this would involve NLP to extract actions and targets from the instruction
    if "search" in instruction:
        return Task(
            description=instruction,
            steps=[
                Step(action="navigate", target="https://www.wikipedia.org"),
                Step(action="click", target="search_input"),
                Step(action="type", target="search_input", value=instruction.replace("search ", "")),
                Step(action="click", target="search_button")
            ]
        )


# Example usage
instruction = "search for the most common species of Canadian ducks"
task = parse_instruction(instruction)
print(json.dumps(task, default=lambda o: o.__dict__, indent=2))
