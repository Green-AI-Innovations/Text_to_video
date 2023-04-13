import cv2
import os

def create_video_with_audio(image_folder, audio_path, video_name):

    print('===========================================================')
    print(image_folder)
    print(audio_path)
    print(video_name)
    import os

    print(os.listdir())
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
