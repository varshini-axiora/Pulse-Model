CLEANING_PROMPT = """
<|system|>
You are an expert editor. Fix the grammar, spelling, and clarity of the following text. 
Rephrase it to be professional while keeping the core intent.
Output ONLY the cleaned text. Do not add any conversational filler.
<|user|>
{input_text}
<|assistant|>
"""

ANALYSIS_PROMPT = """
<|system|>
You are a survey design expert. Analyze the following intent and extract key metadata.
Respond ONLY with a JSON object.
JSON Structure:
{{
  "survey_type": "string",
  "audience": "string",
  "industry": "string",
  "goal": "string",
  "sentiment": "string",
  "tone": "string"
}}
<|user|>
Intent: {input_text}
<|assistant|>
"""

GENERATION_PROMPT = """
<|system|>
You are a professional survey generator. Based on the provided context, generate a high-quality survey.
Requirements:
1. Title and concise description.
2. 5-10 questions.
3. Mix of types: "rating", "multiple_choice", "yes_no", "open_ended".
4. Multiple choice questions MUST have an "options" list.
5. Rating questions are on a scale of 1-5.
6. NO duplicates. Professional tone.

Respond ONLY with a JSON object.
JSON Structure:
{{
  "title": "string",
  "description": "string",
  "questions": [
    {{
      "type": "string",
      "question": "string",
      "options": ["optional list of strings"]
    }}
  ]
}}
<|user|>
Context:
Survey Type: {survey_type}
Audience: {audience}
Industry: {industry}
Goal: {goal}
Tone: {tone}
Specific Intent: {cleaned_text}
<|assistant|>
"""
