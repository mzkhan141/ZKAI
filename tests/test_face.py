"""Unit tests for Face Recognition subsystem."""

import pytest
import numpy as np
from zkai.vision.face import (
    FaceAligner,
    FaceDatabase,
    FaceDetector,
    FaceEmbedding,
    FaceIdentification,
    FaceRecognizer,
    FaceVerification,
)
from zkai.vision.image import Image


def test_face_verification():
    emb1 = np.random.randn(512).tolist()
    emb2 = list(emb1)
    assert FaceVerification.verify(emb1, emb2) is True


def test_face_database_and_identification():
    db = FaceDatabase()
    emb = np.random.randn(512).tolist()
    db.enroll("John Doe", emb)
    assert "John Doe" in db.get_all()

    identifier = FaceIdentification()
    match, sim = identifier.identify(emb, db.get_all())
    assert match == "John Doe"
    assert sim > 0.99
