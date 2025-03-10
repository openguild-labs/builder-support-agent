from ..AI.ai_response import generate_response_with_text
#---------------------------------------------CLASSIFY QUESTION---------------------------------------------------------------#

async def classify_question_with_llm(question):
    """Classify question to 'Trending topic', 'New docs' or 'Other' using LLM"""
    prompt = f"""
    You are an AI that specializes in classifying questions. Read the question below and classify it into one of three categories:

    1. **Trending topic** → If the question is about news, recent trending topic, or blog posts.
    2. **New docs** → If the question is about document updates, new technologies, or pull requests.
    3. **Other** → If it does not belong to either of the above two groups.

    **Return only one of the following three words (no additional text):**
    - "Trending topic"
    - "New docs"
    - "Other"

    Question: "{question}"
    Classification:
    """
    
    response = await generate_response_with_text(prompt)
    result = response.strip()
    valid_labels = {"Trending topic", "New docs", "Other"}
    if result not in valid_labels:
        result = "Other" 

    return result
