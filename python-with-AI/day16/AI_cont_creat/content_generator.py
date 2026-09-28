# content_generator.py

def create_content(generator, topic, platform, tone, language):

    prompt = (
        f"You are a professional social media content creator.\n\n"

        f"Create content in {language}.\n"
        f"Topic: {topic}\n"
        f"Platform: {platform}\n"
        f"Tone: {tone}\n\n"

        f"Create the following:\n"
        f"1. Catchy Title\n"
        f"2. Strong Hook\n"
        f"3. Short Caption\n"
        f"4. 30-second Video Script\n"
        f"5. 5 Hashtags\n"
        f"6. Call to Action\n\n"

        f"Requirements:\n"
        f"- Keep the content clear and engaging.\n"
        f"- Make it suitable for {platform}.\n"
        f"- Use the requested {tone} tone.\n"
        f"- Do not add unnecessary explanations.\n"
        f"- Clearly separate each section."
    )

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.7,
        return_full_text=False
    )

    content = result[0]["generated_text"]

    return content


def generate_ideas(generator, topic):

    prompt = (
        f"Create 5 different social media content ideas "
        f"about {topic}.\n\n"

        f"For each idea provide:\n"
        f"- Title\n"
        f"- Hook\n"
        f"- Short description\n\n"

        f"Make every idea different, creative and engaging."
    )

    result = generator(
        prompt,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.8,
        return_full_text=False
    )

    ideas = result[0]["generated_text"]

    return ideas