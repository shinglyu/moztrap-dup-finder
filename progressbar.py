import sys

class ProgressBar():
    total = 1
    def __init__(self, total = 1):
        self.total = total

    def update(self, progress):
        percent = float(progress)/float(self.total) * 100
        sys.stdout.write("\rProgress: [{0}{1}] {2: 6.2f}%".format('='*int(round(percent/10)), ' '*int(10-round((percent)/10)), percent))
        sys.stdout.flush()
    def done(self):
        self.update(self.total)
        print "\n"
