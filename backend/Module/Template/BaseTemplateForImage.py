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
    image_gen_base_template = """
     beautiful detailed eyes, (eyelashes:1.1), ((8k, RAW photo, highest quality, masterpiece), High detail RAW color photo professional close-up photo, (realistic, photo realism:1.4), (highest quality), (best shadow), (best illustration), ultra high resolution, highly detailed CG unified 8K wallpapers, physics-based rendering, cinematic lighting), (semi-realistic)
    ```
    """

    return image_gen_base_template