from ddgs import DDGS


def web_search(query, max_results=3):
    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:
            return "Sorry, I couldn't find any results."

        response = ""

        for i, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            body = result.get("body", "No description")

            response += f"{i}. {title}\n"
            response += f"{body[:250]}...\n\n"

        return response

    except Exception as e:
        return f"Web search error: {e}"


if __name__ == "__main__":
    query = input("What do you want to search for? ")

    result = web_search(query)

    print("\n" + result)