import face_recognition
import io


def face_locations(image):
    processed_image = face_recognition.load_image_file(io.BytesIO(image))
    return face_recognition.face_locations(processed_image)
