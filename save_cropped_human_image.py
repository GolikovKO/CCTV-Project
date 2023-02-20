import cv2


def save_people_get_off_image(frame, points, people):

    ret = frame[points[1]-130:points[1]+130, points[0]-60:points[0]+60]
    cv2.imwrite('./video_data/people_left/%d.png' % people, ret)


def save_people_get_in_image(frame, points, people):

    ret = frame[points[1]-130 : points[1]+130, points[0]-60 : points[0]+60]
    cv2.imwrite('./video_data/people_in/%d.png' % people, ret)
