"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK CONFIGURATION                             ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define your task-specific settings.                   ║
║  Inherits common settings from core.GenerationConfig                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Symbol Worlds - Symbol Editing - Substitute Symbol task configuration.

    CUSTOMIZE THIS CLASS to add your task's hyperparameters.

    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name
        - difficulty: Optional[str] # Difficulty level
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """

    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════

    domain: str = Field(default="symbol_worlds_symbol_editing")
    image_size: tuple[int, int] = Field(default=(512, 512))

    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════

    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )

    video_fps: int = Field(
        default=15,
        description="Video frame rate"
    )

    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC SETTINGS
    # ══════════════════════════════════════════════════════════════════════════

    symbol_size: int = Field(
        default=60,
        description="Size of each symbol in pixels"
    )

    min_sequence_length: int = Field(
        default=3,
        description="Minimum number of symbols in the sequence"
    )

    max_sequence_length: int = Field(
        default=7,
        description="Maximum number of symbols in the sequence"
    )

    symbol_spacing: int = Field(
        default=80,
        description="Horizontal spacing between symbols in pixels"
    )

    target_border_width: int = Field(
        default=4,
        description="Width of the red border marking the target symbol to substitute"
    )

    target_border_color: tuple[int, int, int] = Field(
        default=(255, 0, 0),
        description="Color of the border marking the target symbol to substitute (red)"
    )

    target_border_padding: int = Field(
        default=8,
        description="Padding between symbol and target border in pixels"
    )
