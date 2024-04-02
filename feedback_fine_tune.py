from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch


from components.feedback import FeedbackSystem

feedback_system = FeedbackSystem()

# Collect feedback for instruction sets
feedback_system.collect_feedback(("What is the capital of France?", ["Navigate to URL: https://www.wikipedia.org/", "Input 'Capital of France' into element by name with value search", "Click element by class_name with value cdx-button.cdx-search-input__end-button", "Click element by xpath with value //a[contains(@href, '/wiki/Paris')]"]), 4)
feedback_system.collect_feedback(("Elon Musk", ["Navigate to URL: https://www.wikipedia.org/", "Click element by id with value js-link-box-en", "Input 'Elon Musk' into element by name with value search", "Click element by class_name with value cdx-button.cdx-search-input__end-button"]), 5)
feedback_system.collect_feedback(("How do plants photosynthesize?", ["Navigate to URL: https://www.wikipedia.org/", "Input 'Photosynthesis' into element by name with value search", "Click element by class_name with value cdx-button.cdx-search-input__end-button", "Click element by xpath with value //a[contains(@href, '/wiki/Photosynthesis')]", "Click element by xpath with value //span[contains(text(), 'Process')]"]), 3)

# Incorporate feedback into the dataset
updated_dataset = feedback_system.incorporate_feedback()

# Print updated dataset
print("Updated dataset with feedback:")
for instruction_set in updated_dataset:
    print("Instruction set:", instruction_set)


model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)


# Modify the serialize_instructions function to handle strings as well as Instruction objects
def serialize_instructions(instructions):
    serialized_instructions = []
    for instr in instructions:
        if isinstance(instr, str):
            # If the instruction is a string, just append it to the list
            serialized_instructions.append(instr)
        elif instr.action_type == "navigate":
            serialized_instructions.append("Navigate to URL: " + instr.input_data)
        elif instr.action_type == "click":
            serialized_instructions.append("Click element by " + instr.target_element["by"] + " with value " + instr.target_element["value"])
        elif instr.action_type == "input":
            serialized_instructions.append("Input '" + instr.input_data + "' into element by " + instr.target_element["by"] + " with value " + instr.target_element["value"])
    return ' -> '.join(serialized_instructions)


# Tokenization
tokenized_dataset = []
for input_text, instructions in updated_dataset:
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    instruction_ids = tokenizer(serialize_instructions(instructions), return_tensors="pt").input_ids
    tokenized_dataset.append((input_ids, instruction_ids))

# Model Configuration
model = T5ForConditionalGeneration.from_pretrained('t5-small')
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

# Training Loop
num_epochs = 10
for epoch in range(num_epochs):
    total_loss = 0.0
    for input_ids, instruction_ids in tokenized_dataset:
        outputs = model(input_ids=input_ids, labels=instruction_ids)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(tokenized_dataset)
    print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss}")

# Save the Model
model.save_pretrained("feedback_model")
