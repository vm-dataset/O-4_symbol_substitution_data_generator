"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK PROMPTS                                   ║
║                                                                               ║
║  Symbol Substitution Task Prompts                                             ║
║                                                                               ║
║  Prompts include {color} and {shape} placeholders that are filled with        ║
║  the specific new symbol information, ensuring unique answers.                ║
║                                                                               ║
║  Example: "Substitute the target symbol with a red circle..."                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
#
#  Each prompt template contains {color} and {shape} placeholders that will be
#  filled with the specific new symbol information (e.g., "red circle",
#  "blue triangle"). This ensures each task has a unique, unambiguous answer.
# ══════════════════════════════════════════════════════════════════════════════

PROMPTS = {
    "default": [
        "Substitute the target symbol with a {color} {shape} in the sequence. The initial image displays a horizontal sequence of symbols, where each symbol is a distinct geometric shape with a specific color. Exactly one symbol in this sequence is marked as the substitution target, indicated by a red rectangular border surrounding it. Your task is to replace only this marked target symbol with a {color} {shape}. The final state must show the sequence with the target symbol substituted by the {color} {shape}, while all other symbols remain unchanged in their original positions. All non-target symbols must retain their original shapes, colors, sequential positions, and visual properties. The substitution operation should affect only the single marked symbol, replacing it with the {color} {shape} at the same position in the sequence.",

        "Perform a symbol substitution operation on the marked target. The scene contains a horizontal sequence of colored geometric symbols arranged from left to right. One specific symbol in this sequence is uniquely identified as the target for substitution by a red border frame drawn around it. No other symbol has this red border marking. Execute the substitution by replacing the marked target symbol with a {color} {shape}. After substitution, all symbols including the newly substituted {color} {shape} must maintain their positions in the sequence, creating a sequence with the same number of symbols as the initial state but with one symbol replaced. The target symbol is unambiguously identified by the red border, ensuring there is no confusion about which symbol to substitute. The new symbol, a {color} {shape}, must appear at the exact position where the target symbol was located.",

        "Execute a symbol editing task to substitute the target symbol with a {color} {shape} in the sequence. The initial state presents a sequence of distinct symbols, each with unique visual characteristics defined by their geometric shape and color combination. Among these symbols, exactly one is designated as the substitution target, clearly marked with a distinctive red rectangular border that surrounds the symbol. This red border provides unambiguous identification of which symbol must be replaced. Your objective is to substitute this specifically marked symbol with a {color} {shape}. The final state should display the sequence with the target symbol replaced by the {color} {shape} at the same sequential position, while all other symbols preserve their original sequential order, visual appearance, and properties. Only the symbol enclosed by the red border should be substituted. The sequence length remains the same, with only the target symbol being replaced by the {color} {shape}.",

        "Replace the marked symbol with a {color} {shape} in the symbol sequence. The task involves a horizontal sequence of symbols where each symbol consists of a colored geometric shape. The sequence contains multiple distinct symbols, and exactly one symbol is marked for substitution using a red rectangular border drawn around it. This red border serves as the sole indicator identifying which symbol must be replaced, eliminating any ambiguity in target selection. Substitute only the symbol that is enclosed by the red border with a {color} {shape}. After the substitution operation, the resulting sequence must contain all symbols in their original positions, with the target symbol replaced by the {color} {shape} at the same location. The substitution affects only the marked symbol, leaving all other symbols unchanged in their visual properties and sequential positions. The total number of symbols in the sequence remains the same before and after the substitution.",
    ],

    "simple": [
        "Substitute the target symbol marked with a red border with a {color} {shape}. Replace only the symbol enclosed by the red rectangular border with a {color} {shape}. All other symbols should remain unchanged in their original positions.",

        "Replace the marked symbol with a {color} {shape} in the sequence. The symbol to substitute is indicated by a red border around it. After substitution, all other symbols should remain in their original sequential order and positions, with only the marked symbol being replaced by a {color} {shape}.",
    ],
}


def get_prompt(task_type: str = "default", new_symbol: dict = None) -> str:
    """
    Select a random prompt for the given task type and fill in the new symbol information.

    Args:
        task_type: Type of task (key in PROMPTS dict)
        new_symbol: Dictionary containing 'shape' and 'color' keys for the new symbol

    Returns:
        Random prompt string with new symbol information filled in
    """
    if new_symbol is None:
        raise ValueError("new_symbol dictionary with 'shape' and 'color' keys is required")

    prompts = PROMPTS.get(task_type, PROMPTS["default"])
    prompt_template = random.choice(prompts)

    # Fill in the color and shape placeholders
    prompt = prompt_template.format(
        color=new_symbol["color"],
        shape=new_symbol["shape"]
    )

    return prompt


def get_all_prompts(task_type: str = "default", new_symbol: dict = None) -> list[str]:
    """
    Get all prompts for a given task type with new symbol information filled in.

    Args:
        task_type: Type of task (key in PROMPTS dict)
        new_symbol: Dictionary containing 'shape' and 'color' keys for the new symbol

    Returns:
        List of prompt strings with new symbol information filled in
    """
    if new_symbol is None:
        raise ValueError("new_symbol dictionary with 'shape' and 'color' keys is required")

    prompt_templates = PROMPTS.get(task_type, PROMPTS["default"])

    # Fill in the color and shape placeholders for all prompts
    prompts = [
        template.format(color=new_symbol["color"], shape=new_symbol["shape"])
        for template in prompt_templates
    ]

    return prompts
