def text_summary_for_image_generation():
    image_gen_template = """
    SYSTEM: You are a helpful text analyzer that knows how to summarize a text. especally character's apperance.
    USER: Summarize this text denoted by backticks:
    ```
    {description}
    ```
    """

    return image_gen_template

def base_image_generation():
    image_gen_template = """
    SYSTEM: You are a helpful text analyzer that knows how to summarize a text. especally character's apperance.
    USER: Summarize this text denoted by backticks:
    ```
    {description}
    ```
    """

    return image_gen_template