import cv2
import numpy as np
import os

class DatasetCreate:
    def __init__(self, face_classifier, data_create):
        self.face_classifier = cv2.CascadeClassifier(face_classifier)
        self.data_create = data_create

    # Load functions
    def face_extractor(self, img):
        # Function detects faces and returns the cropped face
        # If no face detected, it returns the input image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)

        if faces is ():
            return None

        # Crop all faces found
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]

        return cropped_face

    def dataset_create(self):
        # Initialize Webcam
        cap = cv2.VideoCapture(0)
        count = 0

        # Collect 100 samples of your face from webcam input
        while True:

            ret, frame = cap.read()
            if self.face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(self.face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                if not os.path.exists(self.data_create):
                    os.makedirs(self.data_create)

                # Save file in specified directory with unique name
                file_name_path = self.data_create + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # Put count on images and display live count
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)

            else:
                print("Face not found")
                pass

            if cv2.waitKey(1) == 13 or count == 100:  # 13 is the Enter Key
                break

        cap.release()
        cv2.destroyAllWindows()
        print("Collecting Samples Complete")