from sentence_transformers import SentenceTransformer, util
import torch
import logging

logger = logging.getLogger(__name__)

# Initialize model globally to avoid reloading
# Using a small model for CPU efficiency
model = SentenceTransformer('all-MiniLM-L6-v2')

def validate_and_deduplicate(survey_data: dict) -> dict:
    questions = survey_data.get("questions", [])
    if not questions:
        return survey_data

    valid_questions = []
    question_texts = []
    
    for q in questions:
        text = q.get("question", "").strip()
        if not text:
            continue
            
        # Semantic check
        is_duplicate = False
        if question_texts:
            embeddings1 = model.encode([text], convert_to_tensor=True)
            embeddings2 = model.encode(question_texts, convert_to_tensor=True)
            cosine_scores = util.cos_sim(embeddings1, embeddings2)
            
            # If similarity > 0.85, consider it a duplicate
            if torch.max(cosine_scores) > 0.85:
                logger.info(f"Filtered duplicate question: {text}")
                is_duplicate = True
        
        if not is_duplicate:
            valid_questions.append(q)
            question_texts.append(text)
            
    survey_data["questions"] = valid_questions
    return survey_data
