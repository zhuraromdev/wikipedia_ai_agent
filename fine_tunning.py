import logging
from components.instructions import Instruction

from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# from wikipedia_scraper import WikipediaScraper

# instructions_for_query = [
#     Instruction(action_type="navigate", input_data="https://www.wikipedia.org/"),
#     Instruction(action_type="click", target_element={"by": "id", "value": "js-link-box-en"}),
#     Instruction(action_type="input", target_element={"by": "name", "value": "search"}, input_data="Elon Musk"),
#     Instruction(action_type="click", target_element={"by": "class_name", "value": "cdx-button.cdx-search-input__end-button"})
# ]

# scraper = WikipediaScraper()
# scraper.execute_instructions(instructions_for_query)

# Configure logging for transformers
logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

# Initialize model, tokenizer, and optimizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

dataset = [
    ("What is the capital of France?", [
        Instruction(action_type="navigate", input_data="https://www.wikipedia.org/"),
        Instruction(action_type="input", target_element={"by": "name", "value": "search"}, input_data="Capital of France"),
        Instruction(action_type="click", target_element={"by": "class_name", "value": "cdx-button.cdx-search-input__end-button"}),
        Instruction(action_type="click", target_element={"by": "xpath", "value": "//a[contains(@href, '/wiki/Paris')]"})
    ]),
    ("Elon Musk", [
        Instruction(action_type="navigate", input_data="https://www.wikipedia.org/"),
        Instruction(action_type="click", target_element={"by": "id", "value": "js-link-box-en"}),
        Instruction(action_type="input", target_element={"by": "name", "value": "search"}, input_data="Elon Musk"),
        Instruction(action_type="click",
                    target_element={"by": "class_name", "value": "cdx-button.cdx-search-input__end-button"})
    ]),
    ("How do plants photosynthesize?", [
        Instruction(action_type="navigate", input_data="https://www.wikipedia.org/"),
        Instruction(action_type="input", target_element={"by": "name", "value": "search"}, input_data="Photosynthesis"),
        Instruction(action_type="click", target_element={"by": "class_name", "value": "cdx-button.cdx-search-input__end-button"}),
        Instruction(action_type="click", target_element={"by": "xpath", "value": "//a[contains(@href, '/wiki/Photosynthesis')]"}),
        Instruction(action_type="click", target_element={"by": "xpath", "value": "//span[contains(text(), 'Process')]"})
    ]),
]


def serialize_instructions(instructions):
    serialized_instructions = []
    for instr in instructions:
        if instr.action_type == "navigate":
            serialized_instructions.append("Navigate to URL: " + instr.input_data)
        elif instr.action_type == "click":
            serialized_instructions.append("Click element by " + instr.target_element["by"] + " with value " + instr.target_element["value"])
        elif instr.action_type == "input":
            serialized_instructions.append("Input '" + instr.input_data + "' into element by " + instr.target_element["by"] + " with value " + instr.target_element["value"])
    return ' -> '.join(serialized_instructions)


for input_text, instructions in dataset:
    logger.info(f"Processing input: {input_text}")
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Serialize the instructions into a format suitable for the model
    serialized_instructions = serialize_instructions(instructions)
    labels = tokenizer(serialized_instructions, return_tensors="pt").input_ids

    # Forward pass
    outputs = model(input_ids=input_ids, labels=labels)
    loss = outputs.loss
    logger.info(f"Loss: {loss.item()}")

    # Backward pass and optimization
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

model.save_pretrained("NO_feedback_model")


logger.info("Training completed.")
