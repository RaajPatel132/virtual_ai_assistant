import cv2
import numpy as np
import os

try:
    from AIAssistant.features.face_reco.train import Train
except Exception as e:
    print("some module are missing{}".format(e))

class Predict:
    def __init__(self, face_classifier, model):
        self.face_classifier = cv2.CascadeClassifier(face_classifier)
        self.var1 = None
        self.model = model + 'model.yml'

    def face_detector(self, img, size=0.5):
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return img, []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            roi = img[y:y + h, x:x + w]
            roi = cv2.resize(roi, (200, 200))
        return img, roi

    def predict(self):
        # Open Webcam
        cap = cv2.VideoCapture(0)

        while True:

            if not os.path.exists(self.model):
                print('Please First run train model')
                break

            ret, frame = cap.read()

            image, face = self.face_detector(frame)

            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(self.model)


                # Pass face to prediction model
                # "results" comprises of a tuple containing the label and the confidence value
                results = recognizer.predict(face)

                if results[1] < 500:
                    confidence = int(100 * (1 - (results[1]) / 400))
                    display_string = str(confidence) + '% Confident it is User'

                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
                self.var1 = 0
                if confidence > 89:
                    cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Recognition', image)
                    self.var1 = 1
                    break
                else:
                    cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Recognition', image)

            except:
                cv2.putText(image, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Recognition', image)
                pass

            if cv2.waitKey(1) == 13:  # 13 is the Enter Key
                break

        cap.release()
        cv2.destroyAllWindows()