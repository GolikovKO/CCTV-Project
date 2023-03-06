import cv2


def save_cropped_human_image(frame, center_points, human_number):
    cropped_frame = frame[center_points[1] - 130:center_points[1] + 130, center_points[0] - 60:center_points[0] + 60]
    cv2.imwrite('./video_data/people_in/%d.png' % human_number, cropped_frame)
