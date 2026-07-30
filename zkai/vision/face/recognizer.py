"""FaceRecognizer high-level biometric recognition pipeline."""

from typing import Optional, Tuple
from zkai.vision.face.aligner import FaceAligner
from zkai.vision.face.database import FaceDatabase
from zkai.vision.face.detector import FaceDetector
from zkai.vision.face.embedder import FaceEmbedding
from zkai.vision.face.identification import FaceIdentification
from zkai.vision.image import Image


class FaceRecognizer:
    """End-to-end face recognition pipeline: detect -> align -> embed -> identify."""

    def __init__(self):
        self.detector = FaceDetector()
        self.aligner = FaceAligner()
        self.embedder = FaceEmbedding()
        self.identifier = FaceIdentification()
        self.database = FaceDatabase()

    def recognize(self, image: Image) -> Optional[Tuple[str, float]]:
        faces = self.detector.detect_faces(image)
        if not faces:
            return None
        aligned = self.aligner.align(image)
        emb = self.embedder.extract(aligned)
        return self.identifier.identify(emb, self.database.get_all())
