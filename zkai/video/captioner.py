"""VideoCaptioner generating descriptions for video clips."""

from zkai.video.frame_extractor import FrameExtractor
from zkai.vision.captioning import ImageCaptioner


class VideoCaptioner:
    """Generates natural language captions summarizing video content."""

    def __init__(self):
        self.extractor = FrameExtractor()
        self.img_captioner = ImageCaptioner()

    def caption_video(self, video_path: str) -> str:
        frames = self.extractor.extract_keyframes(video_path, stride=60)
        if not frames:
            return "Empty video."
        captions = [self.img_captioner.caption(f) for f in frames[:3]]
        return f"Video showing: {'; '.join(captions)}"
