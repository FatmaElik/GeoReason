"""
Prompt templates for Pilot 01 — Evidence Conflict in VLM Damage Assessment.

The experiment has 5 conditions. Every condition shows the SAME image
(optical patch with a red box around the damaged building) and asks the
same final question. Only the accompanying text changes.

  A  image_only          : no text evidence at all (baseline)
  B  text_consistent     : field report that AGREES with the ground truth
  C  text_conflict       : field report that CONTRADICTS the ground truth
  D  news_conflict       : same contradiction, but written like a news
                           sentence (style inspired by the Turkish
                           Disaster GeoNLP dataset)
  E  conflict_abstain    : same as C, but the model is explicitly allowed
                           to answer "uncertain"

Class names: in the İslahiye subset only classes 3 and 4 appear.
Rename these if your full dataset uses different definitions.
"""

CLASS_NAMES = {
    3: "heavy damage",
    4: "destroyed",
}

# The wrong class used in conflict conditions (binary task: just the other one)
def conflicting_class(true_class: int) -> int:
    return 4 if true_class == 3 else 3


QUESTION = (
    "Look at the building inside the red box. "
    "This satellite image was taken after an earthquake.\n"
    "Classify the damage level of that building.\n"
    "Answer with exactly one option: 'heavy damage' or 'destroyed'."
)

QUESTION_WITH_ABSTAIN = (
    "Look at the building inside the red box. "
    "This satellite image was taken after an earthquake.\n"
    "Classify the damage level of that building.\n"
    "Answer with exactly one option: 'heavy damage', 'destroyed', or 'uncertain'.\n"
    "If the visual evidence and the report disagree and you cannot tell "
    "which one is correct, answer 'uncertain'."
)

# --- text evidence templates -------------------------------------------------

FIELD_REPORT = (
    "A field assessment report about this building states: "
    "\"Ground teams inspected this structure and recorded it as {claim}.\""
)

# News-style sentence. The phrasing imitates how Turkish disaster news
# describes buildings (source of inspiration: Turkish Disaster GeoNLP
# dataset). Kept in English so the language variable stays fixed.
NEWS_REPORT = (
    "A local news article about the earthquake reports: "
    "\"According to residents of the neighbourhood, the building seen in "
    "the image was {claim} in the earthquake.\""
)

NEWS_CLAIM = {
    3: "heavily damaged but left standing",
    4: "completely destroyed",
}


def build_prompt(condition: str, true_class: int) -> str:
    """Return the full text prompt for one condition and one sample."""
    true_name = CLASS_NAMES[true_class]
    wrong_name = CLASS_NAMES[conflicting_class(true_class)]
    wrong_news = NEWS_CLAIM[conflicting_class(true_class)]

    if condition == "A_image_only":
        return QUESTION

    if condition == "B_text_consistent":
        return FIELD_REPORT.format(claim=true_name) + "\n\n" + QUESTION

    if condition == "C_text_conflict":
        return FIELD_REPORT.format(claim=wrong_name) + "\n\n" + QUESTION

    if condition == "D_news_conflict":
        return NEWS_REPORT.format(claim=wrong_news) + "\n\n" + QUESTION

    if condition == "E_conflict_abstain":
        return FIELD_REPORT.format(claim=wrong_name) + "\n\n" + QUESTION_WITH_ABSTAIN

    raise ValueError(f"Unknown condition: {condition}")


CONDITIONS = [
    "A_image_only",
    "B_text_consistent",
    "C_text_conflict",
    "D_news_conflict",
    "E_conflict_abstain",
]


def normalize_answer(raw: str) -> str:
    """Map a free-form model answer to 'heavy damage' / 'destroyed' / 'uncertain' / 'unknown'."""
    text = str(raw).strip().lower()
    has_heavy = "heavy" in text
    has_destroyed = "destroy" in text or "collaps" in text
    has_uncertain = "uncertain" in text or "cannot tell" in text or "not sure" in text

    if has_uncertain and not (has_heavy or has_destroyed):
        return "uncertain"
    if has_heavy and not has_destroyed:
        return "heavy damage"
    if has_destroyed and not has_heavy:
        return "destroyed"
    return "unknown"
