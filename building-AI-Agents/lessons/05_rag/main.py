"""Lesson 05: retrieval-augmented generation.

RAG means retrieving relevant knowledge before answering.
This simple version scores notes by overlapping words with the question.
There is no real model call yet, so the final step only drafts an answer
from retrieved context.
"""

from pathlib import Path


NOTES_PATH = Path(__file__).with_name("notes.txt")
STOP_WORDS = {"a", "an", "and", "is", "it", "of", "the", "to", "what"}


def tokenize(text: str) -> set[str]:
    return {
        cleaned_word
        for word in text.split()
        if (cleaned_word := word.strip(".,?!:;()[]{}").lower())
        and cleaned_word not in STOP_WORDS
    }


def score_notes(question: str, notes: list[str]) -> list[tuple[int, str]]:
    question_words = tokenize(question)

    scored_notes = []
    for note in notes:
        score = len(question_words & tokenize(note))
        scored_notes.append((score, note))

    scored_notes.sort(reverse=True, key=lambda item: item[0])
    return scored_notes


def retrieve(question: str, notes: list[str], limit: int = 2) -> list[str]:
    scored_notes = score_notes(question, notes)
    return [note for score, note in scored_notes[:limit] if score > 0]


def build_rag_prompt(question: str, context: list[str]) -> str:
    joined_context = "\n".join(f"- {note}" for note in context)
    return f"Use this context to answer the question.\n\nContext:\n{joined_context}\n\nQuestion: {question}"


def draft_answer(question: str, context: list[str]) -> str:
    if not context:
        return f"I do not have enough information in my notes to answer: {question}"

    # In a real RAG app, this prompt would be sent to a model.
    prompt = build_rag_prompt(question, context)
    joined_context = " ".join(context)
    return f"{prompt}\n\nDraft answer: Based on the notes, {joined_context}"


def main() -> None:
    notes = [line for line in NOTES_PATH.read_text().splitlines() if line.strip()]
    question = "What is an agent loop?"

    scored_notes = score_notes(question, notes)
    context = retrieve(question, notes)
    print("QUESTION:", question)
    print("SCORED NOTES:")
    for score, note in scored_notes:
        print(f"- score={score}: {note}")
    print("RETRIEVED CONTEXT:", context)
    print("ANSWER:", draft_answer(question, context))

    # TODO: Add a new note to notes.txt and ask a question that retrieves it.
    # TODO: Change limit from 2 to 1 and observe the difference.
    # TODO: Remove misleading notes or improve scoring so bad context is less likely.


if __name__ == "__main__":
    main()
