"""VideoSummarizer for key event extraction."""

from typing import List
from zkai.video.captioner import VideoCaptioner


class VideoSummarizer:
    """Generates textual summary of long-form video content."""

    def __init__(self):
        self.captioner = VideoCaptioner()

    def summarize(self, video_path: str) -> str:
        caption = self.captioner.caption_video(video_path)
        return f"Summary of video '{video_path}': {caption}"
