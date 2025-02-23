# Tool Calling Assistant

## Description

This assistant is intended to be used in a structured manner to create and update issues.json file. This is an example demo project how to implement a custom function calling.

## For this demo
LLM agent populates issues.json file with issues that the user provides


## Dependencies:
- working Ollama and llama3.1 model (or something else, see the `main.py` file)
- poetry installed

### how to setup
```
poetry install
```

### how to test
```
pytest
```

### how to run
```
poetry shell
```

run the llm chatbot which asks for the issue information and writes it to the issues.json file (custom function calling)
```
python structured_assistant/main.py
```

### Final remarks
- The ollama doesn't support function calling perfectly yet bind_tools(tool_choice="auto") is not working as expected.
- the tool_choice="auto" is giving model the ability to either continue normal conversation or call a function.