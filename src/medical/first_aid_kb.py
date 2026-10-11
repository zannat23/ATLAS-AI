"""
ATLAS Medical Module - Expanded First Aid Knowledge Base

Two complementary paths:
1. PHOTO-BASED: wound types visible on skin (handled by the image classifier)
2. SYMPTOM-BASED: emergencies that cannot be diagnosed from a photo
   (fracture, choking, snake bite, electric shock, seizure, poisoning, etc.)
   -- these use a simple guided question/selection flow instead.

Both paths support ITEM-BASED TAILORING: given a list of items the user has
on hand, instructions are adapted to use what's actually available.
"""

# ============================================================
# PART 1: Photo-classifiable wound types (extends classifier.py)
# ============================================================

WOUND_FIRST_AID = {
    'normal': {
        'severity': 1,
        'summary': "No wound detected. You appear to be okay.",
        'steps': [],
    },
    'bruise': {
        'severity': 2,
        'summary': "Bruise / contusion",
        'steps': [
            "Apply a cold compress wrapped in cloth for 15-20 minutes.",
            "Elevate the injured area above heart level if possible.",
            "Rest the area and avoid further impact.",
            "Seek medical help if swelling is severe or doesn't improve in 2-3 days.",
        ],
    },
    'abrasion': {
        'severity': 2,
        'summary': "Abrasion / scrape (skin surface scraped off)",
        'steps': [
            "Rinse the wound gently with clean water to remove dirt and debris.",
            "Clean around the wound with mild soap, avoiding the wound itself.",
            "Pat dry with a clean cloth.",
            "Cover with a sterile dressing to prevent infection.",
            "Change the dressing daily and watch for signs of infection.",
        ],
    },
    'laceration': {
        'severity': 3,
        'summary': "Laceration / cut",
        'steps': [
            "Apply firm, direct pressure with a clean cloth to stop bleeding.",
            "Once bleeding slows, rinse the wound with clean water.",
            "Bring the edges of the wound together and cover with a sterile dressing.",
            "Elevate the area above heart level if possible.",
            "Seek medical help if the cut is deep, won't stop bleeding, or gapes open.",
        ],
    },
    'puncture_wound': {
        'severity': 4,
        'summary': "Puncture wound (nail, splinter, etc.)",
        'steps': [
            "Do NOT remove large embedded objects - stabilize and seek medical help.",
            "For small punctures, let it bleed briefly to help flush out debris.",
            "Clean gently around the wound with water.",
            "Cover with a sterile dressing.",
            "Puncture wounds carry high infection risk - seek medical care, especially for tetanus check.",
        ],
    },
    'burn': {
        'severity': 4,
        'summary': "Burn (severity uncertain from photo alone)",
        'steps': [
            "Cool the burn under running or clean cool water for 10-15 minutes.",
            "Do NOT use ice directly on the burn, and do NOT apply butter, oil, or toothpaste.",
            "Do NOT remove clothing stuck to the burn.",
            "Cover loosely with a clean, non-stick cloth (not fluffy material).",
            "If the burn is larger than your palm, looks white/charred/leathery, has deep blisters, or is on the face/hands/joints, treat as SEVERE - seek emergency medical help immediately.",
            "For any burn, if in doubt, seek medical help - it's always safer to have it checked.",
        ],
    },
    'insect_bite': {
        'severity': 2,
        'summary': "Insect bite / sting",
        'steps': [
            "If a stinger is visible, scrape it out sideways (don't squeeze/tweeze).",
            "Wash the area with soap and water.",
            "Apply a cold compress to reduce swelling.",
            "Watch for allergic reaction: difficulty breathing, swelling of face/throat, hives - seek emergency help immediately if these occur.",
        ],
    },
    'rash_allergic': {
        'severity': 3,
        'summary': "Rash / allergic skin reaction",
        'steps': [
            "Remove the person from the suspected trigger (plant, substance, food).",
            "Wash the area gently with cool water.",
            "Avoid scratching the area.",
            "If rash spreads rapidly, or breathing becomes difficult, treat as a severe allergic reaction - this is an emergency.",
        ],
    },
    'frostbite': {
        'severity': 4,
        'summary': "Frostbite",
        'steps': [
            "Move to a warm area immediately.",
            "Remove wet clothing and jewelry from the affected area.",
            "Warm the area gradually with body heat or warm (not hot) water - do NOT use direct heat like a fire or heater.",
            "Do NOT rub or massage the frostbitten area.",
            "Seek medical help - severe frostbite needs professional care.",
        ],
    },
    'infection': {
        'severity': 4,
        'summary': "Infected wound",
        'steps': [
            "Clean gently with clean water - do NOT squeeze or drain pus yourself.",
            "Cover with a clean dressing.",
            "Watch for spreading redness, warmth, fever, or red streaking - these need urgent medical care.",
            "Seek medical help for antibiotics if infection is present.",
        ],
    },
}

# ============================================================
# PART 2: Symptom-based emergency guides (NOT photo-diagnosable)
# ============================================================

SYMPTOM_GUIDES = {
    'fracture': {
        'label': "Suspected broken bone / fracture",
        'severity': 5,
        'steps': [
            "Do NOT try to straighten or realign the limb.",
            "Immobilize the area using a splint (a rolled newspaper, stick, or board works) tied gently above and below the injury.",
            "Apply a cold compress wrapped in cloth to reduce swelling - do not apply directly to skin.",
            "If the bone is visibly protruding, cover loosely with a clean cloth - do NOT push it back in.",
            "Seek emergency medical help immediately. Keep the person still.",
        ],
    },
    'choking': {
        'label': "Choking",
        'severity': 5,
        'steps': [
            "Ask 'Are you choking?' - if they can cough or speak, encourage them to keep coughing.",
            "If they cannot breathe, cough, or speak: stand behind them, give 5 sharp back blows between the shoulder blades with the heel of your hand.",
            "If that doesn't work, give 5 abdominal thrusts (Heimlich maneuver): fist above the navel, grasp with other hand, pull sharply inward and upward.",
            "Alternate 5 back blows and 5 abdominal thrusts until the object is dislodged or help arrives.",
            "If the person becomes unconscious, begin CPR and call for emergency help immediately.",
        ],
    },
    'snake_bite': {
        'label': "Snake bite",
        'severity': 5,
        'steps': [
            "Keep the person calm and still - movement speeds venom spread.",
            "Keep the bitten limb lower than the heart.",
            "Remove any tight clothing or jewelry near the bite before swelling starts.",
            "Do NOT cut the wound, suck out venom, or apply a tight tourniquet.",
            "Note the snake's appearance if safely possible, but do not risk another bite.",
            "Seek emergency medical help immediately - antivenom may be needed.",
        ],
    },
    'electric_shock': {
        'label': "Electric shock",
        'severity': 5,
        'steps': [
            "Do NOT touch the person if they are still in contact with the electrical source.",
            "Turn off the power source if possible, or use a dry, non-conductive object (wooden stick) to separate them from the source.",
            "Once safe, check breathing and pulse - begin CPR if needed.",
            "Cover any burns with a clean, dry cloth.",
            "Seek emergency medical help immediately, even if the person seems fine - internal injuries can be delayed.",
        ],
    },
    'seizure': {
        'label': "Seizure",
        'severity': 4,
        'steps': [
            "Do NOT restrain the person or put anything in their mouth.",
            "Clear the area of hard or sharp objects.",
            "Cushion their head with something soft.",
            "Turn them onto their side once the shaking stops, to help keep the airway clear.",
            "Time the seizure - if it lasts more than 5 minutes, or another starts right after, seek emergency help immediately.",
        ],
    },
    'unconscious_breathing': {
        'label': "Unconscious but breathing",
        'severity': 5,
        'steps': [
            "Turn the person onto their side (recovery position) to keep the airway clear.",
            "Tilt their head back slightly to help breathing.",
            "Check breathing continuously until help arrives.",
            "Do NOT give them anything to eat or drink.",
            "Seek emergency medical help immediately.",
        ],
    },
    'not_breathing': {
        'label': "Not breathing / no pulse",
        'severity': 5,
        'steps': [
            "Call for emergency help immediately, or have someone else call while you start CPR.",
            "Place hands in the center of the chest, push hard and fast (about 2 inches deep, 100-120 compressions per minute).",
            "Give 30 chest compressions, then 2 rescue breaths if trained - if untrained, continue compressions only.",
            "Continue until the person responds or emergency help arrives.",
        ],
    },
    'poisoning': {
        'label': "Poisoning / suspected ingestion of harmful substance",
        'severity': 5,
        'steps': [
            "Do NOT induce vomiting unless specifically told to by a medical professional.",
            "Try to identify what was ingested and how much - keep the container/packaging if available.",
            "If the person is unconscious, place them in the recovery position and check breathing.",
            "Seek emergency medical help immediately.",
        ],
    },
    'heatstroke': {
        'label': "Heatstroke / severe heat exhaustion",
        'severity': 5,
        'steps': [
            "Move the person to a cool, shaded area immediately.",
            "Remove excess clothing.",
            "Cool them down with cool (not ice-cold) water, wet cloths, or fanning.",
            "If conscious, give small sips of water - do not force fluids.",
            "Seek emergency medical help immediately, especially if confused or unconscious.",
        ],
    },
    'nosebleed': {
        'label': "Nosebleed",
        'severity': 2,
        'steps': [
            "Sit upright and lean slightly forward (do not tilt the head back).",
            "Pinch the soft part of the nose firmly for 10-15 minutes without releasing.",
            "Breathe through the mouth.",
            "Apply a cold compress to the bridge of the nose.",
            "Seek medical help if bleeding doesn't stop after 20-30 minutes or is heavy.",
        ],
    },
}

# ============================================================
# PART 3: Item-based tailoring
# ============================================================

ITEM_SUBSTITUTES = {
    "bandage":        ["clean cloth", "torn t-shirt", "scarf", "sanitary pad"],
    "sterile dressing": ["clean cloth", "ironed cotton cloth", "clean cotton wool"],
    "ice":            ["frozen vegetables wrapped in cloth", "cold wet cloth", "cold metal spoon"],
    "antiseptic":     ["soap and clean water", "salt water rinse"],
    "splint":         ["rolled newspaper", "stick", "ruler", "board", "rolled magazine"],
    "gauze":          ["clean cloth strips", "clean cotton cloth"],
    "cold compress":  ["ice wrapped in cloth", "cold wet towel", "frozen food packet wrapped in cloth"],
    "clean water":    ["boiled and cooled water", "bottled water"],
    "tape":           ["cloth strips tied", "rubber band (for small dressings)"],
}

def get_tailored_first_aid(condition_key: str, available_items: list = None, is_symptom_guide: bool = False) -> dict:
    """
    Return first-aid steps for a condition, noting which available items can
    be used for each step (via ITEM_SUBSTITUTES), so guidance stays useful
    even without a fully-stocked first-aid kit.
    """
    source = SYMPTOM_GUIDES if is_symptom_guide else WOUND_FIRST_AID
    entry = source.get(condition_key)
    if not entry:
        return {"error": f"Unknown condition: {condition_key}"}

    available_items = [i.lower().strip() for i in (available_items or [])]
    steps = entry['steps']
    annotated_steps = []

    for step in steps:
        note = None
        step_lower = step.lower()
        for ideal_item, substitutes in ITEM_SUBSTITUTES.items():
            if ideal_item in step_lower:
                if ideal_item in available_items:
                    note = f"You have {ideal_item} - use it directly."
                else:
                    matched = [s for s in substitutes if s in available_items]
                    if matched:
                        note = f"No {ideal_item}? You can use: {matched[0]}."
        annotated_steps.append({"instruction": step, "item_note": note})

    return {
        "condition": condition_key,
        "label": entry.get('summary', entry.get('label', condition_key)),
        "severity": entry['severity'],
        "steps": annotated_steps,
    }