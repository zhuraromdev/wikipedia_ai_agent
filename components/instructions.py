class Instruction:
    def __init__(self, action_type, target_element=None, input_data=None, conditionals=None, metadata=None):
        self.action_type = action_type
        self.target_element = target_element
        self.input_data = input_data
        self.conditionals = conditionals
        self.metadata = metadata


navigate_to_wikipedia = Instruction(
    action_type="navigate",
    input_data="https://www.wikipedia.org/"
)

click_english = Instruction(
    action_type="click",
    target_element={"by": "id", "value": "js-link-box-en"}
)

input_search_term = Instruction(
    action_type="input",
    target_element={"by": "name", "value": "search"},
    input_data="Artificial Intelligence"  # Example search term
)

click_search = Instruction(
    action_type="click",
    target_element={"by": "class_name", "value": "cdx-button.cdx-search-input__end-button"}
)

navigate_to_article = Instruction(
    action_type="navigate",
    input_data="https://en.wikipedia.org/wiki/Roman_Empire"  # Example article URL
)
