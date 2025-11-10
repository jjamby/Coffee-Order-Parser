import re
import datetime

DRINKS = ["coffee", "latte", "espresso", "cappuccino", "americano"]
MODIFIERS = ["sugar", "milk", "cream", "syrup", "ice", "ice cream"]
SIZES = ["small", "medium", "large"]

def parse_order(text):
    """
    Validate if the order text follows proper grammar structure.
    Returns True if valid, False otherwise.
    """
    text = text.lower().strip()
    
    # Check if any drink is mentioned
    has_drink = any(drink in text for drink in DRINKS)
    if not has_drink:
        return False
    
    # Basic validation patterns
    patterns = [
        r"(order|want|make|get|need)\s+(\d+\s+)?(\w+)",
        r"(\d+\s+)?(\w+)\s+(please|with)",
        r"(a|an)\s+(\w+)",
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    
    return False

def extract_order(text):
    """
    Extract order details from the text.
    Returns a dictionary with quantity, drink, and modifiers.
    """
    text = text.lower().strip()
    
    # Extract quantity
    quantity_match = re.search(r'(\d+)', text)
    quantity = int(quantity_match.group(1)) if quantity_match else 1
    
    # Extract drink
    drink = None
    for d in DRINKS:
        if d in text:
            drink = d.capitalize()
            break
    
    # Extract size
    size = None
    for s in SIZES:
        if s in text:
            size = s.capitalize()
            break

    # Extract modifiers, prioritizing longer phrases
    found_modifiers = []
    for mod in sorted(MODIFIERS, key=len, reverse=True):
        if mod in text and not any(mod in existing for existing in found_modifiers):
            found_modifiers.append(mod)

    return {
        "quantity": quantity,
        "drink": drink,
        "size": size,
        "modifiers": ", ".join(found_modifiers) if found_modifiers else "none",
        "created_at": datetime.datetime.now().strftime("%d/%m/%Y")
    }
