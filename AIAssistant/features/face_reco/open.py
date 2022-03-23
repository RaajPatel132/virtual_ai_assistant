import subprocess
import os

try:
    from AIAssistant.features.face_reco.predict import Predict
    from AIAssistant.features.face_reco.train import Train
except Exception as e:
    print("some module are missing{}".format(e))

class Open():
    def __init__(self):
        pass

    def launch_app(self, path_of_app):
        try:
            subprocess.call([path_of_app])
            return True
        except Exception as e:
            print(e)
            return False

    def luanchingApp(self, var1, app_path):

        if var1 == 1:
            self.launch_app(app_path)

        else:
            print("can't open app because your face is not recognized!")