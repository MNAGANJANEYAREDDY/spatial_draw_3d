from dataclasses import dataclass, field
from typing import List, Optional
import time
import uuid


@dataclass
class SlideMetadata:
    """Metadata describing a slide."""
    id: str
    created_at: float
    title: Optional[str] = None


@dataclass
class Slide:
    """A single slide scene containing strokes and metadata."""
    metadata: SlideMetadata
    strokes: List = field(default_factory=list)


class SlideManager:
    """
    Professional slide scene manager.

    Responsibilities:
    - Manage slide lifecycle
    - Maintain history
    - Provide safe navigation
    - Track metadata
    - Prepare exportable slide data
    """

    def __init__(self):

        self._slides: List[Slide] = []
        self._current_index: int = 0

        self._create_initial_slide()

    # --------------------------------------------------
    # Slide creation
    # --------------------------------------------------

    def _create_initial_slide(self):

        metadata = SlideMetadata(
            id=str(uuid.uuid4()),
            created_at=time.time(),
            title="Slide 1"
        )

        slide = Slide(metadata=metadata)
        self._slides.append(slide)

    def create_slide(self, title: Optional[str] = None):

        metadata = SlideMetadata(
            id=str(uuid.uuid4()),
            created_at=time.time(),
            title=title or f"Slide {len(self._slides)+1}"
        )

        slide = Slide(metadata=metadata)
        self._slides.append(slide)

        self._current_index = len(self._slides) - 1

        return slide

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    def next_slide(self):

        if self._current_index == len(self._slides) - 1:
            self.create_slide()
        else:
            self._current_index += 1

        return self.current_slide()

    def previous_slide(self):

        if self._current_index > 0:
            self._current_index -= 1

        return self.current_slide()

    def goto_slide(self, index: int):

        if 0 <= index < len(self._slides):
            self._current_index = index

        return self.current_slide()

    # --------------------------------------------------
    # Slide operations
    # --------------------------------------------------

    def add_stroke(self, stroke):

        self.current_slide().strokes.append(stroke)

    def clear_slide(self):

        self.current_slide().strokes.clear()

    # --------------------------------------------------
    # Accessors
    # --------------------------------------------------

    def current_slide(self) -> Slide:

        return self._slides[self._current_index]

    def strokes(self):

        return self.current_slide().strokes

    def slide_index(self):

        return self._current_index

    def slide_count(self):

        return len(self._slides)

    # --------------------------------------------------
    # Export hooks
    # --------------------------------------------------

    def export_data(self):

        """
        Prepares slide data for export systems
        such as PDF or image rendering.
        """

        export_payload = []

        for slide in self._slides:

            export_payload.append({
                "id": slide.metadata.id,
                "created_at": slide.metadata.created_at,
                "title": slide.metadata.title,
                "stroke_count": len(slide.strokes),
                "strokes": slide.strokes
            })

        return export_payload