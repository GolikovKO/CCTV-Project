import cv2

class SaveImage():

    def savePeopleGetOff(self, frame, points, people):

        ret = frame[points[1]-130:points[1]+130, points[0]-60:points[0]+60]
        cv2.imwrite('D:\Dev\\vsCodeProjects\CCTV\\video_data\people_left\%d.png' % people, ret)

    def savePeopleGetIn(self, frame, points, people):

        ret = frame[points[1]-130 : points[1]+130, points[0]-60 : points[0]+60]
        cv2.imwrite('D:\Dev\\vsCodeProjects\CCTV\\video_data\people_in\%d.png' % people, ret)