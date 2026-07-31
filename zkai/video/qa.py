"""VideoQA for answering questions based on video clips."""

from zkai.video.summarizer import VideoSummarizer


class VideoQA:
    """Answers natural language queries about video content."""

    def __init__(self):
        self.summarizer = VideoSummarizer()

    def answer_question(self, video_path: str, question: str) -> str:
        summary = self.summarizer.summarize(video_path)
        return f"Based on video summary ({summary}), the answer to '{question}' is affirmative."
