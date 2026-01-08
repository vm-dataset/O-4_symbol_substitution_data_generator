# Symbol Substitution Data Generator

A synthetic data generator for symbol editing reasoning tasks focused on target symbol substitution.

---

## Overview

This generator creates visual reasoning tasks that demonstrate symbol substitution operations. Each task shows a horizontal sequence of distinct symbols with one symbol marked for substitution, challenging the model to identify and replace the target symbol with a new symbol while maintaining all other symbols unchanged in their original positions.

**Task Type**: Symbol Worlds - Symbol Editing

**Template ID**: `Symbol Worlds_SymbolEditing_3`

**Template Name**: Substitute Symbol

**Domain**: `symbol_worlds_symbol_editing`

---

## Quick Start

```bash
# 1. Navigate to project directory
cd data_gen

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate tasks
python examples/generate.py --num-samples 50
```

---

## Task Description

### Initial State
- White background
- A horizontal sequence of colored geometric symbols
- Each symbol has a unique shape-color combination
- One symbol is marked with a red rectangular border (the substitution target)

### Task
Substitute the symbol marked with the red border with a specific new symbol. The task prompt explicitly specifies the exact color and shape of the new symbol (e.g., "substitute with a red circle" or "substitute with a blue triangle"), ensuring the answer is unique and unambiguous. The target symbol to be replaced is identified by the red rectangular border surrounding it. After substitution, all symbols including the newly substituted one must maintain their original positions in the sequence.

### Final State
- Same white background
- The sequence with the target symbol replaced by a new symbol
- All symbols remain in their original positions
- The new symbol occupies the same position as the original target symbol

### Video (Optional)
Animated transition showing:
1. Initial state with target marked
2. Target symbol gradually transforming into the new symbol
3. Red border fading during transformation
4. Final state with target substituted

---

## Output Format

Each task generates:

```
data/questions/symbol_worlds_symbol_editing_task/{task_id}/
├── first_frame.png          # Initial state: sequence with target marked
├── final_frame.png          # Final state: sequence after substitution with specified symbol
├── prompt.txt               # Task instruction specifying the exact new symbol (color + shape)
└── ground_truth.mp4         # Solution video showing substitution process (optional)
```

**Example Prompt**: "Substitute the target symbol with a red circle in the sequence. The initial image displays a horizontal sequence of symbols, where each symbol is a distinct geometric shape with a specific color. Exactly one symbol in this sequence is marked as the substitution target, indicated by a red rectangular border surrounding it. Your task is to replace only this marked target symbol with a red circle..."

---

## Symbol Design Rules

**Ensures Unambiguous Task and Unique Answer:**

- **Symbol Uniqueness**: Each symbol in a sequence has a unique shape-color combination
- **Target Marking**: Exactly one symbol is marked with a red rectangular border for substitution
- **Visual Clarity**: The red border provides unambiguous identification of the substitution target
- **Explicit New Symbol Specification**: The prompt explicitly specifies both the color and shape of the new symbol (e.g., "orange star", "blue triangle"), ensuring the answer is completely unique
- **Answer Uniqueness**: Since the prompt specifies the exact new symbol, there is only one correct answer for each task
- **New Symbol Distinctness**: The new symbol is guaranteed to be visually distinct from all existing symbols in the sequence

**Available Shapes:**
- Circle
- Square
- Triangle (equilateral)
- Star (5-pointed)
- Diamond
- Hexagon

**Available Colors:**
- Red (220, 50, 50)
- Blue (50, 100, 220)
- Green (50, 180, 50)
- Yellow (230, 200, 50)
- Purple (180, 50, 180)
- Orange (255, 140, 50)
- Cyan (50, 200, 200)
- Pink (255, 100, 150)

**Total Unique Combinations**: 6 shapes × 8 colors = 48 possible unique symbols

---

## Configuration

Customize generation in `src/config.py`:

```python
domain: str = "symbol_worlds_symbol_editing"
image_size: tuple[int, int] = (512, 512)
symbol_size: int = 60                       # Symbol size in pixels
min_sequence_length: int = 3                # Minimum symbols in sequence
max_sequence_length: int = 7                # Maximum symbols in sequence
symbol_spacing: int = 80                    # Horizontal spacing between symbols
target_border_width: int = 4                # Red border line width
target_border_color: tuple = (255, 0, 0)    # Border color for substitution target (red)
target_border_padding: int = 8              # Padding between symbol and border
generate_videos: bool = True                # Enable video generation
video_fps: int = 15                         # Video frame rate
```

---

## Examples

### Generate with specific seed
```bash
python examples/generate.py --num-samples 100 --seed 42
```

### Generate without videos
```bash
python examples/generate.py --num-samples 50 --no-videos
```

### Custom output directory
```bash
python examples/generate.py --num-samples 50 --output data/my_tasks
```

---

## Project Structure

```
data_gen/
├── core/                    # Framework utilities (do not modify)
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # Task implementation
│   ├── generator.py        # Symbol substitution task generator
│   ├── prompts.py          # Prompt templates
│   └── config.py           # Configuration
├── examples/
│   └── generate.py         # Entry point
└── data/questions/         # Generated output
```

---

## Requirements

- Python >= 3.8
- numpy >= 1.26.4
- Pillow >= 10.4.0
- pydantic >= 2.10.5
- opencv-python >= 4.10.0 (for video generation)

---

## Task Properties

### Unambiguous Task with Unique Answer

The task design ensures zero ambiguity and a single correct answer:

1. **Visual Marking**: The red rectangular border uniquely identifies the target symbol
2. **Unique Symbols**: Each symbol has a distinct shape-color combination
3. **Explicit New Symbol**: The prompt explicitly specifies the exact color and shape of the new symbol (e.g., "red circle", "blue triangle")
4. **Single Correct Answer**: Because the prompt specifies the exact new symbol, there is only one correct final state
5. **Single Target**: Exactly one symbol is marked for substitution in each task
6. **Distinct New Symbol**: The new symbol is guaranteed to be visually different from all existing symbols

### Visual Reasoning

The task demonstrates visual symbol manipulation:

- Symbol transformation and replacement
- Sequence position preservation
- Spatial relationships between symbols
- Visual identification and substitution

---

## Video Animation Details

The ground truth video shows a smooth substitution process:

1. **Hold Initial State** (8 frames): Shows all symbols with target marked
2. **Transformation Phase** (30 frames): Target symbol gradually morphs into new symbol via cross-fade effect
3. **Hold Final State** (8 frames): Shows final sequence with target substituted

Total duration: ~3 seconds at 15 fps

---

## License

MIT License
