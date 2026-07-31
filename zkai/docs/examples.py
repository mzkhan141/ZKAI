"""ExampleGenerator producing runnable code examples."""

class ExampleGenerator:
    """Generates runnable usage examples for facade methods."""

    def generate_examples(self) -> str:
        return "```python\nfrom zkai import *\nai = ZKAI()\nai.chat('Hello world')\n```"
