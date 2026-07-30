"""Vision, Multimodal, OCR, Detection, and Image Processing for ZKAI."""

from zkai.vision.image import Image
from zkai.vision.video import Video
from zkai.vision.camera import Camera
from zkai.vision.detection import ObjectDetector, BoundingBox, DetectionResult
from zkai.vision.ocr import OCREngine
from zkai.vision.captioning import ImageCaptioner
from zkai.vision.classification import ImageClassifier, ClassificationResult
from zkai.vision.segmentation import ImageSegmenter, Mask
from zkai.vision.face import FaceDetector, FaceResult
from zkai.vision.features import FeatureExtractor
from zkai.vision.encoder import VisionEncoder

__all__ = [
    "Image",
    "Video",
    "Camera",
    "ObjectDetector",
    "BoundingBox",
    "DetectionResult",
    "OCREngine",
    "ImageCaptioner",
    "ImageClassifier",
    "ClassificationResult",
    "ImageSegmenter",
    "Mask",
    "FaceDetector",
    "FaceResult",
    "FeatureExtractor",
    "VisionEncoder",
]
