from enum import Enum

class GY2T:
	class MainState(Enum):
		started = auto()
		stopped = auto()
	class RoadState(Enum):
		straight = auto()
		turning = auto()
	class DriveState(Enum):
		advancing = auto() #proceeding in the path without gps info. just go straight and-or turn accordingly
		passenger = auto() #carrying passenger, must advance to the next station
		parking = auto() #indicates that car is in process of moving to an appropriate parking position 
		parked = auto() #car has parked and parkour has finished
	class DefinitionSubject(Enum):
		""" Instead of auto, labels will be paired with corresponding ids in the model """
		obstacle = auto()
		station = auto()
		parkingSign = auto()
		#...

	class LinesNotDetectedError(Exception):
		pass

	def __init__(self):
		self.autonomous = Autonomous()
		self.vision = Vision()
		self.mainState = MainState.stopped
		self.driveState = -1
		self.roadState = -1
		firstVision = self.vision.result
		result = self.autonomous.firstProceed(self.vision.result)
		pass

	class Vision:
		self.model = Sequential()
		#...
		def __init__(self):
			pass
			
		def predict(self, img):
			#model.predict_classes(img)
			pass

	class Autonomous:
		def __init__(self):
			pass

		def firstProceed():
			#start movement. look for lines, signs, etc. if no signs, just move forward
			pass

		def mainControl(self, parent):
			if parent.mainState == MainState.stopped:
				try:
					result = firstProceed()
					if(result):
						parent.mainState = MainState.started
					#...
				except LinesNotDetectedError:
					pass

			if parent.driveState == DriveState.parked:
				#finish up
				pass

			pass

		def park():
			pass
				