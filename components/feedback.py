from typing import List, Tuple


class FeedbackSystem:
    def __init__(self):
        self.dataset_with_feedback = []

    def collect_feedback(self, instruction_set: Tuple[str, List[str]], feedback: int):
        """
        Collects feedback for an instruction set.

        Args:
        - instruction_set (Tuple[str, List[str]]): Tuple containing the input text and corresponding instructions.
        - feedback (int): User feedback rating.

        Returns:
        - None
        """
        self.dataset_with_feedback.append((instruction_set, feedback))

    def incorporate_feedback(self) -> List[Tuple[str, List[str]]]:
        """
        Incorporates user feedback into the dataset of instructions.

        Returns:
        - updated_dataset (List[Tuple[str, List[str]]]): Updated dataset with user feedback.
        """
        updated_dataset = []
        for instruction_set, feedback in self.dataset_with_feedback:
            # Adjust instructions based on user feedback, if necessary
            # For simplicity, we'll assume the feedback is an integer rating (e.g., 1 to 5)
            # You can adjust the instructions or their weights based on the feedback rating
            if feedback < 3:
                # Example: Reduce the weight of these instructions or remove them from the dataset
                instruction_set = (instruction_set[0], instruction_set[1][:-1])  # Remove the last instruction
            elif feedback > 3:
                # Example: Add more instructions or increase their weight in the dataset
                instruction_set[1].append("Click element by class_name with value next-page")  # Add an additional instruction

            updated_dataset.append(instruction_set)

        return updated_dataset

