import cv2


def save_cropped_human_image(human_flag, frame, center_points, human_number):
    cropped_frame = frame[center_points[1] - 130:center_points[1] + 130, center_points[0] - 60:center_points[0] + 60]
    if human_flag is 1:
        path = 'people_in'
    else:
        path = 'people_left'
    cv2.imwrite(f'./source/video_data/{path}/%d.png' % human_number, cropped_frame)
