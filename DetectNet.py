from mtcnn import MTCNN
detector = MTCNN()


def Detect(pic):
    result = detector.detect_faces(pic)
    if len(result) > 0 :
        if result[0]["confidence"] < 0.7:
            return None
        return result[0]["box"]
    return None