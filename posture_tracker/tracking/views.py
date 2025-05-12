import cv2
import numpy as np
import mediapipe as mp
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_http_methods

# Initialize MediaPipe Pose solution
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

# Global variables for counting repetitions
pushup_stage = ''
pushup_counter = 0

squat_stage = ''
squat_counter = 0

bicep_stage = ''
bicep_counter = 0

pullup_stage = ''
pullup_counter = 0

# Utility function to add text to frame
def add_counter_to_frame(frame, counter, exercise_name):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'{exercise_name} Counter: {counter}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Streaming function to return raw frames
def generate_frames(exercise_name, stage, counter, update_stage):
    cap = cv2.VideoCapture(0)  # Capture video from the default camera
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(106, 13, 173), thickness=4, circle_radius=5),
            mp_drawing.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10)
        )

        try:
            landmarks = results.pose_landmarks.landmark

            if update_stage(landmarks):  # Call the stage update logic passed as parameter
                counter += 1

        except Exception as e:
            print(f"Error during {exercise_name} processing: {e}")

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        add_counter_to_frame(image, counter, exercise_name)

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (frame)  # Send raw frame bytes

# Functions for stage updates
def update_pushup_stage(landmarks):
    global pushup_stage
    shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

    if shoulder_y < hip_y:
        if pushup_stage == "down":
            pushup_stage = "up"
            return True
    else:
        pushup_stage = "down"
    return False

def update_squat_stage(landmarks):
    global squat_stage
    hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
    knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y

    if hip_y < knee_y:
        if squat_stage == "down":
            squat_stage = "up"
            return True
    else:
        squat_stage = "down"
    return False

def update_bicep_stage(landmarks):
    global bicep_stage
    elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
    wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y

    if elbow_y < wrist_y:
        if bicep_stage == "down":
            bicep_stage = "up"
            return True
    else:
        bicep_stage = "down"
    return False

def update_pullup_stage(landmarks):
    global pullup_stage
    shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

    if shoulder_y < hip_y:
        if pullup_stage == "down":
            pullup_stage = "up"
            return True
    else:
        pullup_stage = "down"
    return False

# Views for each exercise
@require_http_methods(["GET"])
def track_pushups(request):
    global pushup_counter
    return StreamingHttpResponse(generate_frames("Pushup", pushup_stage, pushup_counter, update_pushup_stage),
                                 content_type='image/jpeg')

@require_http_methods(["GET"])
def track_squats(request):
    global squat_counter
    return StreamingHttpResponse(generate_frames("Squat", squat_stage, squat_counter, update_squat_stage),
                                 content_type='image/jpeg')

@require_http_methods(["GET"])
def track_bicep_curls(request):
    global bicep_counter
    return StreamingHttpResponse(generate_frames("Bicep Curl", bicep_stage, bicep_counter, update_bicep_stage),
                                 content_type='image/jpeg')

@require_http_methods(["GET"])
def track_pullups(request):
    global pullup_counter
    return StreamingHttpResponse(generate_frames("Pull-up", pullup_stage, pullup_counter, update_pullup_stage),
                                 content_type='image/jpeg')
