import cv2
import csv
import os

# Initialize an empty list to store the label data (optional, for in-memory tracking)
label_data = []

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

# Load the video file
video_file = "path_to_file.mp4"  # Replace with your actual video file path

# Generate the CSV file name based on the video file name
video_filename = os.path.basename(video_file)  # Extracts 'L1P1C2I.mp4'
csv_filename = os.path.splitext(video_filename)[0] + ".csv"  # Converts to 'L1P1C2I.csv'

# Initialize the CSV file
initialize_csv(csv_filename)

cap = cv2.VideoCapture(video_file)

# Initialize variables to store frame numbers
start_frame = None
end_frame = None

# Get video frame rate to calculate frame delay
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 30  # Fallback to a default value if FPS is not available

# Get total frame count
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Flag to check if the video is paused
paused = False
current_frame = 0
fast_mode = False  # Flag for 10x speed mode (mapped to 'C')
faster_mode = False  # Flag for 2x speed mode (mapped to 'Z')
xfast_mode = False  # Flag for 5x speed mode (mapped to 'X')

# Label input mode and buffer
label_input_mode = False
label_buffer = ""

# New variable to store the default label
default_label = None

# Ensure the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Controls legend to display in the top right corner
controls_legend = [
    "Controls:",
    "SPACE: Play/Pause",
    "C: Play 10x Speed",
    "X: Play 5x Speed",
    "Z: Play 2x Speed",
    "D/RIGHT: Next Frame",
    "A/LEFT: Prev Frame",
    "J: Jump to Frame",
    "F: Jump Backward 10s",
    "G: Jump Forward 10s",
    "S: Set Start Frame",
    "E: Set End Frame & Label",
    "M: Set Default Label",
    "Q: Quit"
]

def display_legend(frame):
    """Displays the legend text on the top right corner of the frame."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 255, 0)  # Green (same as frame number) in BGR format
    thickness = 1
    line_type = cv2.LINE_AA
    
    x_offset = frame.shape[1] - 250  # Adjust x position to the right side of the frame
    y_offset = 30  # Start from the top, and adjust y position
    
    for i, line in enumerate(controls_legend):
        y_position = y_offset + i * 20  # 20 pixels gap between lines
        cv2.putText(frame, line, (x_offset, y_position), font, font_scale, font_color, thickness, line_type)

print("Controls displayed on video.")

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
                    1, (0, 255, 0), 2, cv2.LINE_AA)  # Green color for the frame number

        # Display label input if in input mode
        if label_input_mode:
            label_text = f"Label: {label_buffer}"
            cv2.putText(frame, label_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display the legend on the top right corner
        display_legend(frame)

        # Display the frame
        cv2.imshow('Video Labeling Tool', frame)

    # Set delay based on the mode (normal, 2x, 5x, or 10x speed)
    if fast_mode:
        wait_time = int(1000 / (fps * 10))
    elif xfast_mode:
        wait_time = int(1000 / (fps * 5))
    elif faster_mode:
        wait_time = int(1000 / (fps * 2))
    else:
        wait_time = int(1000 / fps)

    key = cv2.waitKey(wait_time) & 0xFF

    if label_input_mode:
        # Input numbers while in label input mode
        if ord('0') <= key <= ord('9'):
            label_buffer += chr(key)
        elif key == ord('\r') or key == 13:  # Enter key
            # Append the label to CSV
            if start_frame is not None and label_buffer.isdigit():
                label = int(label_buffer)
                if 0 <= label <= 70:
                    # Append to in-memory list and CSV
                    label_data.append([start_frame, end_frame, label])
                    append_to_csv(csv_filename, [start_frame, end_frame, label])
                    print(f"Label recorded: Start={start_frame}, End={end_frame}, Label={label}")
                    # Reset input mode and buffer
                    label_input_mode = False
                    label_buffer = ""
                    start_frame = None  # Reset start frame for next labeling
                else:
                    print("Invalid label. Please enter a number between 0 and 70.")
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
            # Record the end frame and use default label if set, otherwise prompt for label input
            if start_frame is not None:
                end_frame = current_frame
                print(f"End frame recorded: {end_frame}")
                if default_label is not None:
                    # Use the default label
                    label = default_label
                    label_data.append([start_frame, end_frame, label])
                    append_to_csv(csv_filename, [start_frame, end_frame, label])
                    print(f"Label recorded: Start={start_frame}, End={end_frame}, Label={label}")
                    start_frame = None  # Reset start frame for next labeling
                else:
                    print("*******ENTER ACTION LABEL PLEASE*******")
                    label_input_mode = True
                    label_buffer = ""
            else:
                print("No start frame recorded. Press 'S' to record the start frame before pressing 'E'.")

        elif key == ord('m'):
            # Set default label
            default_label_input = input("Enter default label (0-70): ")
            if default_label_input.isdigit():
                default_label = int(default_label_input)
                if 0 <= default_label <= 70:
                    print(f"Default label set to: {default_label}")
                else:
                    print("Invalid label. Please enter a number between 0 and 70.")
                    default_label = None
            else:
                print("Invalid input. Default label not set.")
                default_label = None

        elif key == ord(' '):
            # Toggle pause/resume at normal speed
            paused = not paused
            fast_mode = False  # Disable 10x speed
            faster_mode = False  # Disable 2x speed
            xfast_mode = False  # Disable 5x speed
            print(f"Video {'paused' if paused else 'resumed at normal speed'}.")

        elif key == ord('c'):  # Play at 10x speed
            paused = False
            fast_mode = True  # Enable 10x speed
            faster_mode = False  # Disable 2x speed
            xfast_mode = False  # Disable 5x speed
            print("Playing video at 10x speed.")

        elif key == ord('z'):  # Play at 2x speed
            paused = False
            faster_mode = True  # Enable 2x speed
            fast_mode = False  # Disable 10x speed
            xfast_mode = False  # Disable 5x speed
            print("Playing video at 2x speed.")

        elif key == ord('x'):  # Play at 5x speed
            paused = False
            xfast_mode = True  # Enable 5x speed
            fast_mode = False  # Disable 10x speed
            faster_mode = False  # Disable 2x speed
            print("Playing video at 5x speed.")

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
                        display_legend(frame)  # Re-display legend after stepping frames
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
                    display_legend(frame)  # Re-display legend after stepping frames
                    cv2.imshow('Video Labeling Tool', frame)
                    print(f"Moved backward to frame: {current_frame}")
                else:
                    print("Warning: Could not retrieve the previous frame.")
            else:
                print("Video is playing. Pause it before stepping frames.")

        elif key == ord('j') and paused:  # 'j' key to jump to a specific frame
            frame_number = int(input(f"Enter a frame number between 0 and {total_frames - 1}: "))
            if 0 <= frame_number < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                if ret:
                    current_frame = frame_number
                    frame_text = f"Frame: {current_frame}/{total_frames}"
                    cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2, cv2.LINE_AA)
                    display_legend(frame)  # Re-display legend after jumping
                    cv2.imshow('Video Labeling Tool', frame)
                    print(f"Jumped to frame: {current_frame}")
                else:
                    print("Error: Could not retrieve the specified frame.")
            else:
                print(f"Invalid frame number. Please enter a number between 0 and {total_frames - 1}.")

        elif key == ord('f') and paused:  # 'f' key to jump backward 10 seconds
            frames_to_jump = int(10 * fps)  # Calculate how many frames correspond to 10 seconds
            new_frame = max(current_frame - frames_to_jump, 0)  # Ensure we don't go below frame 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            ret, frame = cap.read()
            if ret:
                current_frame = new_frame
                frame_text = f"Frame: {current_frame}/{total_frames}"
                cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                display_legend(frame)  # Re-display legend after jumping
                cv2.imshow('Video Labeling Tool', frame)
                print(f"Jumped backward 10 seconds to frame: {current_frame}")
            else:
                print("Error: Could not retrieve the specified frame.")

        elif key == ord('g') and paused:  # 'g' key to jump forward 10 seconds
            frames_to_jump = int(10 * fps)  # Calculate how many frames correspond to 10 seconds
            new_frame = min(current_frame + frames_to_jump, total_frames - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            ret, frame = cap.read()
            if ret:
                current_frame = new_frame
                frame_text = f"Frame: {current_frame}/{total_frames}"
                cv2.putText(frame, frame_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                display_legend(frame)  # Re-display legend after jumping
                cv2.imshow('Video Labeling Tool', frame)
                print(f"Jumped forward 10 seconds to frame: {current_frame}")
            else:
                print("Error: Could not retrieve the specified frame.")

        elif key == ord('q'):
            # Quit the program
            print("Quitting the application.")
            break

# Release resources and close windows
cap.release()
cv2.destroyAllWindows()
