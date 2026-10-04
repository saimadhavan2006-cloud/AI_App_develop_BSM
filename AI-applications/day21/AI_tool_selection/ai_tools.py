def recommend_ai_tool(task_description):
    task = task_description.lower()

    if "pdf" in task or "document" in task or "notes" in task:
        return "Recommended Tool: Google NotebookLM (Best for document-grounded research)."

    elif "search" in task or "news" in task or "real-time" in task:
        return "Recommended Tool: Perplexity AI (Best for web search with direct citations)."

    elif "code" in task or "reasoning" in task or "writing" in task:
        return "Recommended Tool: Anthropic Claude (Best for deep reasoning & programming)."

    else:
        return "Recommended Tool: General Purpose LLM (ChatGPT / Gemini)."


print(recommend_ai_tool(
    "I need to summarize a 50-page PDF report"
))

print(recommend_ai_tool(
    "Find recent news on space missions with references"
))