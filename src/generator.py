"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK GENERATOR                                 ║
║                                                                               ║
║  Symbol Substitution Task Generator                                           ║
║  Generates tasks with unique answers by specifying the exact new symbol       ║
║  (color + shape) in the prompt.                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import math
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class TaskGenerator(BaseGenerator):
    """
    Symbol Worlds - Symbol Editing - Substitute Symbol task generator.

    Generates tasks showing symbol substitution in a sequence.

    Required:
        - generate_task_pair(task_id) -> TaskPair

    The base class provides:
        - self.config: Your TaskConfig instance
        - generate_dataset(): Loops and calls generate_task_pair() for each sample
    """

    # Define available shapes and colors for symbols
    SHAPES = ["circle", "square", "triangle", "star", "diamond", "hexagon"]
    COLORS = {
        "red": (220, 50, 50),
        "blue": (50, 100, 220),
        "green": (50, 180, 50),
        "yellow": (230, 200, 50),
        "purple": (180, 50, 180),
        "orange": (255, 140, 50),
        "cyan": (50, 200, 200),
        "pink": (255, 100, 150),
    }

    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)

        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")

    def generate_task_pair(self, task_id: str) -> TaskPair:
        """
        Generate one symbol substitution task pair with unique answer.

        The prompt explicitly specifies the new symbol's color and shape,
        ensuring only one correct answer exists.
        """

        # Generate task data (symbol sequence, target index, new symbol)
        task_data = self._generate_task_data()

        # Render images
        first_image = self._render_initial_state(task_data)
        final_image = self._render_final_state(task_data)

        # Generate video (optional)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(first_image, final_image, task_id, task_data)

        # Select prompt with new symbol information
        prompt = get_prompt(
            task_type=task_data.get("type", "default"),
            new_symbol=task_data["new_symbol"]
        )

        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path
        )

    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC METHODS
    # ══════════════════════════════════════════════════════════════════════════

    def _generate_task_data(self) -> dict:
        """
        Generate random symbol substitution task configuration.

        Creates:
        - A sequence of unique symbols (shape + color combinations)
        - A target index indicating which symbol to substitute
        - A new symbol to replace the target symbol (randomly generated but unique)
        - Symbol positions in the sequence

        The new symbol information (color + shape) will be embedded in the prompt
        to ensure a unique, unambiguous answer.
        """
        # Random sequence length
        sequence_length = random.randint(
            self.config.min_sequence_length,
            self.config.max_sequence_length
        )

        # Generate unique symbol sequence
        symbols = self._generate_unique_symbol_sequence(sequence_length)

        # Random target index (which symbol to substitute)
        target_index = random.randint(0, sequence_length - 1)

        # Generate a new symbol that is different from all existing symbols
        new_symbol = self._generate_new_symbol(symbols)

        # Calculate positions for horizontal sequence
        symbol_positions = self._calculate_symbol_positions(sequence_length)

        # Create substituted symbols (after replacement)
        substituted_symbols = [
            new_symbol if i == target_index else s
            for i, s in enumerate(symbols)
        ]

        return {
            "symbols": symbols,
            "target_index": target_index,
            "new_symbol": new_symbol,
            "symbol_positions": symbol_positions,
            "substituted_symbols": substituted_symbols,
            "type": "default"
        }

    def _generate_unique_symbol_sequence(self, length: int) -> list:
        """
        Generate a sequence of unique symbols.

        Each symbol is a dict with 'shape', 'color', and 'color_rgb'.
        Ensures each symbol in the sequence is visually distinct.
        """
        # Create pool of all possible shape-color combinations
        all_combinations = []
        for shape in self.SHAPES:
            for color_name, color_rgb in self.COLORS.items():
                all_combinations.append({
                    "shape": shape,
                    "color": color_name,
                    "color_rgb": color_rgb
                })

        # Randomly sample unique symbols
        if length > len(all_combinations):
            raise ValueError(f"Requested sequence length {length} exceeds available unique combinations {len(all_combinations)}")

        return random.sample(all_combinations, length)

    def _generate_new_symbol(self, existing_symbols: list) -> dict:
        """
        Generate a new symbol that is different from all existing symbols.

        Args:
            existing_symbols: List of existing symbols in the sequence

        Returns:
            A new symbol dict with 'shape', 'color', and 'color_rgb'
        """
        # Create pool of all possible shape-color combinations
        all_combinations = []
        for shape in self.SHAPES:
            for color_name, color_rgb in self.COLORS.items():
                all_combinations.append({
                    "shape": shape,
                    "color": color_name,
                    "color_rgb": color_rgb
                })

        # Remove existing symbols from the pool
        existing_combos = [
            (s["shape"], s["color"]) for s in existing_symbols
        ]

        available_combinations = [
            combo for combo in all_combinations
            if (combo["shape"], combo["color"]) not in existing_combos
        ]

        if not available_combinations:
            raise ValueError("No available unique symbol combinations left")

        return random.choice(available_combinations)

    def _calculate_symbol_positions(self, count: int) -> list:
        """
        Calculate x-positions for symbols in a horizontal sequence.

        Centers the sequence horizontally in the image.
        """
        width, height = self.config.image_size
        total_width = count * self.config.symbol_spacing

        # Center the sequence
        start_x = (width - total_width) // 2 + self.config.symbol_spacing // 2
        y = height // 2

        positions = []
        for i in range(count):
            x = start_x + i * self.config.symbol_spacing
            positions.append((x, y))

        return positions

    def _render_initial_state(self, task_data: dict) -> Image.Image:
        """
        Render initial state: symbol sequence with target marked by red border.

        Layout:
        - White background
        - Horizontal sequence of symbols
        - Target symbol marked with red rectangular border
        """
        width, height = self.config.image_size
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        symbols = task_data["symbols"]
        positions = task_data["symbol_positions"]
        target_index = task_data["target_index"]

        # Draw all symbols
        for i, (symbol, pos) in enumerate(zip(symbols, positions)):
            self._draw_symbol(draw, symbol, pos)

            # Draw red border around target symbol to substitute
            if i == target_index:
                self._draw_target_border(draw, pos)

        return img

    def _render_final_state(self, task_data: dict) -> Image.Image:
        """
        Render final state: symbol sequence after target substitution.

        Shows the sequence with the target symbol replaced by the new symbol.
        """
        width, height = self.config.image_size
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        substituted_symbols = task_data["substituted_symbols"]
        positions = task_data["symbol_positions"]

        # Draw substituted symbols
        for symbol, pos in zip(substituted_symbols, positions):
            self._draw_symbol(draw, symbol, pos)

        return img

    def _draw_symbol(self, draw: ImageDraw.Draw, symbol: dict, position: tuple):
        """
        Draw a symbol at the specified position.

        Args:
            draw: ImageDraw object
            symbol: Dict with 'shape' and 'color_rgb'
            position: (x, y) center position
        """
        x, y = position
        size = self.config.symbol_size
        half_size = size // 2
        color = symbol["color_rgb"]
        shape = symbol["shape"]

        if shape == "circle":
            draw.ellipse(
                [x - half_size, y - half_size, x + half_size, y + half_size],
                fill=color,
                outline=(0, 0, 0),
                width=2
            )

        elif shape == "square":
            draw.rectangle(
                [x - half_size, y - half_size, x + half_size, y + half_size],
                fill=color,
                outline=(0, 0, 0),
                width=2
            )

        elif shape == "triangle":
            points = [
                (x, y - half_size),  # Top
                (x - half_size, y + half_size),  # Bottom left
                (x + half_size, y + half_size)   # Bottom right
            ]
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)

        elif shape == "star":
            points = self._get_star_points(x, y, half_size, 5)
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)

        elif shape == "diamond":
            points = [
                (x, y - half_size),  # Top
                (x + half_size, y),  # Right
                (x, y + half_size),  # Bottom
                (x - half_size, y)   # Left
            ]
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)

        elif shape == "hexagon":
            points = self._get_regular_polygon_points(x, y, half_size, 6)
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)

    def _get_star_points(self, cx: float, cy: float, radius: float, points: int) -> list:
        """Generate points for a star shape."""
        star_points = []
        angle_step = math.pi / points
        inner_radius = radius * 0.4

        for i in range(points * 2):
            angle = i * angle_step - math.pi / 2
            r = radius if i % 2 == 0 else inner_radius
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            star_points.append((x, y))

        return star_points

    def _get_regular_polygon_points(self, cx: float, cy: float, radius: float, sides: int) -> list:
        """Generate points for a regular polygon."""
        points = []
        angle_step = 2 * math.pi / sides

        for i in range(sides):
            angle = i * angle_step - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))

        return points

    def _draw_target_border(self, draw: ImageDraw.Draw, position: tuple):
        """
        Draw red rectangular border around target symbol.

        Args:
            draw: ImageDraw object
            position: (x, y) center position of symbol
        """
        x, y = position
        size = self.config.symbol_size
        padding = self.config.target_border_padding
        half_size = size // 2 + padding

        draw.rectangle(
            [x - half_size, y - half_size, x + half_size, y + half_size],
            outline=self.config.target_border_color,
            width=self.config.target_border_width
        )

    def _generate_video(
        self,
        first_image: Image.Image,
        final_image: Image.Image,
        task_id: str,
        task_data: dict
    ) -> str:
        """Generate animation showing symbol substitution process."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"

        # Create animation frames
        frames = self._create_substitution_animation(task_data)

        result = self.video_generator.create_video_from_frames(
            frames,
            video_path
        )

        return str(result) if result else None

    def _create_substitution_animation(
        self,
        task_data: dict,
        hold_frames: int = 8,
        transition_frames: int = 30
    ) -> list:
        """
        Create animation frames showing symbol substitution process.

        Animation:
        1. Hold initial state (all symbols visible, target marked with red border)
        2. Transition: Target symbol gradually transforms into the new symbol
        3. Hold final state (target symbol substituted, all symbols in place)
        """
        frames = []
        width, height = self.config.image_size

        # Initial frames
        initial_frame = self._render_initial_state(task_data)
        for _ in range(hold_frames):
            frames.append(initial_frame.copy())

        symbols = task_data["symbols"]
        positions = task_data["symbol_positions"]
        target_index = task_data["target_index"]
        new_symbol = task_data["new_symbol"]

        # Transition frames: morph target symbol to new symbol
        for i in range(transition_frames):
            img = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(img)

            progress = (i + 1) / transition_frames

            # Draw all symbols
            for j, (symbol, pos) in enumerate(zip(symbols, positions)):
                if j == target_index:
                    # Draw morphing symbol (from old to new)
                    self._draw_morphing_symbol(img, draw, symbol, new_symbol, pos, progress)
                    # Draw fading red border in the first half
                    if progress < 0.5:
                        self._draw_target_border(draw, pos)
                else:
                    # Draw normal symbols
                    self._draw_symbol(draw, symbol, pos)

            frames.append(img)

        # Final frames
        final_frame = self._render_final_state(task_data)
        for _ in range(hold_frames):
            frames.append(final_frame.copy())

        return frames

    def _draw_morphing_symbol(
        self,
        img: Image.Image,
        draw: ImageDraw.Draw,
        old_symbol: dict,
        new_symbol: dict,
        position: tuple,
        progress: float
    ):
        """
        Draw a morphing symbol transitioning from old to new.

        Uses cross-fade effect: old symbol fades out while new symbol fades in.

        Args:
            img: Image to draw on
            draw: ImageDraw object
            old_symbol: Original symbol dict
            new_symbol: New symbol dict
            position: (x, y) center position
            progress: Transition progress from 0.0 to 1.0
        """
        # Cross-fade: old symbol alpha decreases, new symbol alpha increases
        old_alpha = 1.0 - progress
        new_alpha = progress

        # Draw old symbol with fading alpha
        if old_alpha > 0.01:
            self._draw_symbol_with_alpha(img, draw, old_symbol, position, old_alpha)

        # Draw new symbol with increasing alpha
        if new_alpha > 0.01:
            self._draw_symbol_with_alpha(img, draw, new_symbol, position, new_alpha)

    def _draw_symbol_with_alpha(
        self,
        img: Image.Image,
        draw: ImageDraw.Draw,
        symbol: dict,
        position: tuple,
        alpha: float
    ):
        """
        Draw a symbol with transparency effect.

        Creates a semi-transparent version by blending with background.
        """
        # Create a temporary image with the symbol
        temp = Image.new('RGBA', img.size, (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp)

        # Draw symbol on temp image
        x, y = position
        size = self.config.symbol_size
        half_size = size // 2
        color = symbol["color_rgb"]
        shape = symbol["shape"]

        # Apply alpha to color
        alpha_color = tuple(list(color) + [int(255 * alpha)])

        if shape == "circle":
            temp_draw.ellipse(
                [x - half_size, y - half_size, x + half_size, y + half_size],
                fill=alpha_color,
                outline=(0, 0, 0, int(255 * alpha)),
                width=2
            )

        elif shape == "square":
            temp_draw.rectangle(
                [x - half_size, y - half_size, x + half_size, y + half_size],
                fill=alpha_color,
                outline=(0, 0, 0, int(255 * alpha)),
                width=2
            )

        elif shape == "triangle":
            points = [
                (x, y - half_size),
                (x - half_size, y + half_size),
                (x + half_size, y + half_size)
            ]
            temp_draw.polygon(points, fill=alpha_color, outline=(0, 0, 0, int(255 * alpha)), width=2)

        elif shape == "star":
            points = self._get_star_points(x, y, half_size, 5)
            temp_draw.polygon(points, fill=alpha_color, outline=(0, 0, 0, int(255 * alpha)), width=2)

        elif shape == "diamond":
            points = [
                (x, y - half_size),
                (x + half_size, y),
                (x, y + half_size),
                (x - half_size, y)
            ]
            temp_draw.polygon(points, fill=alpha_color, outline=(0, 0, 0, int(255 * alpha)), width=2)

        elif shape == "hexagon":
            points = self._get_regular_polygon_points(x, y, half_size, 6)
            temp_draw.polygon(points, fill=alpha_color, outline=(0, 0, 0, int(255 * alpha)), width=2)

        # Composite temp image onto main image
        img.paste(temp, (0, 0), temp)
