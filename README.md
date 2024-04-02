# Web Browsing Agent

This project aims to develop a basic AI agent capable of navigating a browser to search Wikipedia and retrieve relevant information based on user queries. The project is divided into several levels, each building upon the previous one to enhance the functionality and performance of the agent.

## Level 1

### Description:
Create a basic AI agent that navigates a browser using Selenium to search Wikipedia. The agent should be able to accept user queries and retrieve information from Wikipedia pages.

### Implementation:
- Python script using Selenium library to automate web browsing.
- The script prompts the user for a query and searches Wikipedia using the query.
- It extracts relevant information from the Wikipedia page, splits the content into paragraphs, and analyzes the content using pre-trained word embeddings (e.g., GloVe) to find the most similar paragraph to the user query.
- Displays the relevant information to the user.

### Usage:
To run the agent:
1. Install the necessary dependencies `pip install -r requirements.txt`.
2. Run the Python script `python3 main.py`.
3. Enter a query when prompted and observe the agent's behavior.

## Level 2

### Description:
Create an instruction set for the AI agent to accomplish tasks efficiently. Define the schema for the instruction set and provide examples.

### Implementation:
- Define a schema for the instruction set, specifying actions, target elements, and input data.
- Provide examples of instruction sets for common tasks such as navigating to a URL, clicking elements, and entering text.

### Usage:
- Run the Python script `python3 fine_tunning.py` 

### Example Instruction Set Schema:
```python
InstructionSet = [
    {
        "action": "navigate",
        "target_element": None,
        "input_data": "https://www.wikipedia.org/"
    },
    {
        "action": "input",
        "target_element": {"by": "name", "value": "search"},
        "input_data": "Search query"
    },
    {
        "action": "click",
        "target_element": {"by": "class_name", "value": "search-button"},
        "input_data": None
    }
]
```

### Output after run:
```shell
    INFO:__main__:Processing input: What is the capital of France?
    INFO:__main__:Loss: 5.529930114746094
    INFO:__main__:Processing input: Elon Musk
    INFO:__main__:Loss: 8.689251899719238
    INFO:__main__:Processing input: How do plants photosynthesize?
    INFO:__main__:Loss: 6.319988250732422
    INFO:__main__:Training completed.
```

## Level 3
Provide a feedback system for collecting working instructions to further fine tune the model.

### Description:
The agent employs the Transformer architecture, specifically T5ForConditionalGeneration from the Transformers library, for model training. The training process involves:

- Tokenization: Converting text inputs and instruction sets into numerical tokens suitable for model input.
- Training Loop: Optimizing the model parameters using the tokenized dataset through multiple epochs.
- Model Saving: Once trained, the model is saved for future use as feedback_model.

### Usage:
- Run the Python script `python3 feedback_fine_tune.py` 

### Output after run:
```shell
    Epoch 1/10, Average Loss: 6.853562037150065
    Epoch 2/10, Average Loss: 5.662357648213704
    Epoch 3/10, Average Loss: 5.115714391072591
    Epoch 4/10, Average Loss: 4.723679542541504
    Epoch 5/10, Average Loss: 4.415220578511556
    Epoch 6/10, Average Loss: 4.1500022411346436
    Epoch 7/10, Average Loss: 3.921599547068278
    Epoch 8/10, Average Loss: 3.7141262690226235
    Epoch 9/10, Average Loss: 3.5151754220326743
    Epoch 10/10, Average Loss: 3.3244860967000327
```


# Future improvement

### Advanced NLP Techniques:
- Implement state-of-the-art natural language processing techniques, such as transformer-based models like BERT or GPT, to enhance the agent's understanding of user queries and improve search accuracy.
- Explore techniques for handling ambiguous queries and understanding context to provide more relevant responses.

### Task Automation Extensions:
- Expand the agent's capabilities beyond Wikipedia to handle a wider range of web-based tasks, such as filling out forms, interacting with APIs, or scraping data from dynamic websites.
- Incorporate machine learning models for web data extraction and interpretation to enable the agent to perform more complex tasks autonomously.

### Reinforcement Learning Framework:
- Implement a reinforcement learning framework to enable the agent to learn from its interactions with users and adapt its behavior over time.
- Develop reward mechanisms to encourage desirable behaviors and penalize undesirable ones, facilitating continuous improvement and adaptation.

### Parallelization and Distributed Computing:
- Explore techniques for parallelizing web browsing tasks and distributing workload across multiple instances to improve efficiency and scalability.
- Utilize cloud computing resources to dynamically scale the agent's capacity based on demand and handle large volumes of queries more effectively.

### Data Encryption and Secure Communication:
- Implement encryption mechanisms to secure user data and communications between the AI agent and web sources, ensuring privacy and confidentiality.
- Integrate authentication and authorization mechanisms to control access to sensitive information and prevent unauthorized use of the agent.

### Enhanced Feedback Collection:
- Develop more sophisticated feedback mechanisms to collect detailed user feedback, including ratings, comments, and suggestions.
- Implement user engagement analytics to track user interactions and identify areas for improvement in the AI agent's performance.

### Feedback Analysis and Integration:
- Utilize natural language processing techniques to analyze user feedback and extract actionable insights for model improvement.
- Integrate feedback analysis into the model training pipeline to automatically update the agent's behavior based on user input.

### Interactive Feedback Loop:
- Implement an interactive feedback loop where the AI agent can actively engage with users to clarify queries, address concerns, and gather additional information to improve task execution.
- Enable the AI agent to adapt its behavior in real-time based on user feedback, fostering a dynamic and responsive user experience.