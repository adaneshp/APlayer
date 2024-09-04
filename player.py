import cv2
import csv
import os

# Initialize an empty list to store the label data (optional, for in-memory tracking)
label_data = []

# CSV file where the labels will be saved
csv_file = "labels.csv"

# Function to initialize the CSV file with headers if it doesn't exist
def initialize_csv(csv_file):
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Start Frame", "End Frame", "Label"])
            print(f"CSV file '{csv_file}' created with headers.")

# Function to append a row to the CSV file
def append_to_csv(csv_file, row):
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        print(f"Row written to CSV: {row}")

# Initialize the CSV file
initialize_csv(csv_file)

# Load the video file
video_file = "/path/to/your/video.mp4"  # Replace with your actual video file path
cap = cv2.VideoCapture(video_file)

# Initialize variables to store frame numbers
start_frame = None
end_frame = None

# Get video frame rate to calculate frame delay
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 60  # Fallback to a default value if FPS is not available

# Get total frame count
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Flag to check if the video is paused
paused = False
current_frame = 0

# Label input mode and buffer
label_input_mode = False
label_buffer = ""

# Ensure the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

print("Controls:")
print("  S - Record Start Frame")
print("  E - Record End Frame and Input Label")
print("  SPACE - Pause/Resume Video")
print("  D or RIGHT ARROW - Move Forward One Frame (when paused)")
print("  A or LEFT ARROW - Move Backward One Frame (when paused)")
print("  Q - Quit and Exit")

while cap.isOpened():
    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("End of video reached.")
            break

        # Get the current frame number
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # Overlay the frame number on the video
        frame_text = f"Frame: {current_frame}/{total_frames}"
        cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display label input if in input mode
        if label_input_mode:
            label_text = f"Label: {label_buffer}"
            cv2.putText(frame, label_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Video Labeling Tool', frame)

    # Wait for key press with appropriate delay
    key = cv2.waitKey(int(1000 / fps)) & 0xFF

    if label_input_mode:
        # Input numbers while in label input mode
        if ord('0') <= key <= ord('9'):
            label_buffer += chr(key)
        elif key == ord('\r') or key == 13:  # Enter key
            # Append the label to CSV
            if start_frame is not None and label_buffer.isdigit():
                label = int(label_buffer)
                if 1 <= label <= 69:
                    # Append to in-memory list and CSV
                    label_data.append([start_frame, end_frame, label])
                    append_to_csv(csv_file, [start_frame, end_frame, label])
                    print(f"Label recorded: Start={start_frame}, End={end_frame}, Label={label}")
                    # Reset input mode and buffer
                    label_input_mode = False
                    label_buffer = ""
                else:
                    print("Invalid label. Please enter a number between 1 and 60.")
            else:
                print("Label input canceled or invalid input.")
                label_input_mode = False
                label_buffer = ""
        elif key == ord('\b'):  # Backspace key
            label_buffer = label_buffer[:-1]
        elif key == ord(' '):  # Space to exit input mode
            label_input_mode = False
            label_buffer = ""

    else:
        # Handle key presses when not in input mode
        if key == ord('s'):
            # Record the start frame
            start_frame = current_frame
            print(f"Start frame recorded: {start_frame}")

        elif key == ord('e'):
            # Record the end frame and prompt for label input
            if start_frame is not None:
                end_frame = current_frame
                print(f"End frame recorded: {end_frame}")
                print("*******ENTER ACTION LABEL PLEASE*******")
                label_input_mode = True
                label_buffer = ""
            else:
                print("No start frame recorded. Press 'S' to record the start frame before pressing 'E'.")

        elif key == ord(' '):
            # Toggle pause/resume
            paused = not paused
            print(f"Video {'paused' if paused else 'resumed'}.")

        elif key == ord('d') or key == 2555904:  # 'd' key or RIGHT ARROW
            if paused:
                new_frame = current_frame + 1
                if new_frame < total_frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                    ret, frame = cap.read()
                    if ret:
                        current_frame = new_frame
                        frame_text = f"Frame: {current_frame}/{total_frames}"
                        cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 255, 0), 2, cv2.LINE_AA)
                        cv2.imshow('Video Labeling Tool', frame)
                        print(f"Moved forward to frame: {current_frame}")
                    else:
                        print("Warning: Could not retrieve the next frame.")
                else:
                    print("Already at the last frame.")
            else:
                print("Video is playing. Pause it before stepping frames.")

        elif key == ord('a') or key == 2424832:  # 'a' key or LEFT ARROW
            if paused:
                new_frame = max(current_frame - 1, 0)
                cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                ret, frame = cap.read()
                if ret:
                    current_frame = new_frame
                    frame_text = f"Frame: {current_frame}/{total_frames}"
                    cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow('Video Labeling Tool', frame)
                    print(f"Moved backward to frame: {current_frame}")
                else:
                    print("Warning: Could not retrieve the previous frame.")
            else:
                print("Video is playing. Pause it before stepping frames.")

        elif key == ord('q'):
            # Quit the program
            print("Quitting the application.")
            break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
