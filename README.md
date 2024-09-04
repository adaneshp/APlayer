# APlayer: A Simple Video Player and Labeling Tool

## A Note

This is not a complicated program. It is just a simple script. I needed a lightweight player that displays the frame number and allows me to move forward and backward for labeling a series of videos. I wrote it to improve efficiency and make my work/life easier :-) If you have any specific requests for additions, feel free to leave a comment. If I find the time, I will update the code or help you figure it out.

I don't usually share all the projects and code I develop, but I felt this one saved me a lot of time, so I wanted to share it with everyone. I hope it helps!

## Overview

This script provides a simple tool for labeling sections within a video file. Users can navigate through the video, mark start and end frames for labels, and assign numerical labels to the captured segments. The labels are saved into a CSV file for further processing or analysis.

## Features

- **Video Playback**: View video and track current frame.
- **Pause/Resume**: Pause and resume video playback to select specific frames.
- **Frame-by-frame Navigation**: Move forward or backward by one frame when paused.
- **Labeling**: Select a start and end frame, then assign a label.
- **CSV Export**: Saves labels (start frame, end frame, label) to a CSV file.
  
## Prerequisites

Before running the script, ensure you have the following Python packages installed:

```bash
pip install opencv-python
```

## How It Works

The script allows you to play a video and use keyboard shortcuts to mark start and end frames. After marking the end frame, you will be prompted to input a label that occurred between the start and end frames. The labels are saved into a CSV file along with the corresponding frame range.

### Key Controls

- **S**: Mark the current frame as the start.
- **E**: Mark the current frame as the end and input a label.
- **SPACE**: Pause or resume the video.
- **D or RIGHT ARROW**: Move forward by one frame when the video is paused.
- **A or LEFT ARROW**: Move backward by one frame when the video is paused.
- **Q**: Quit the application.

### Labeling

1. Press `S` to mark the start frame.
2. Press `E` to mark the end frame and input a label (valid labels are integers).
3. The labeled data will be saved to a CSV file in the format: `Start Frame`, `End Frame`, `Label`.

### CSV File Format

A CSV file named `labels.csv` is automatically created (if not already present) in the working directory. The CSV contains three columns:

- **Start Frame**: The frame number where the label starts.
- **End Frame**: The frame number where the label ends.
- **Label**: The numeric label assigned to the selected section.

Example CSV content:
```
Start Frame,End Frame,Label
100,200,5
250,300,3
```

## Usage

1. Replace the video file path in the script with your actual video file path:

    ```python
    video_file = "/path/to/your/video.mp4"  # Replace with your actual video file path
    ```

2. Run the script:

    ```bash
    python video_labeling_tool.py
    ```

3. Use the controls to navigate through the video, mark sequences, and assign labels.

4. After labeling, check the `labels.csv` file in the working directory for saved data.

## Script Breakdown

### Main Components:

- **initialize_csv**: Ensures that the CSV file has appropriate headers if it doesn't already exist.
- **append_to_csv**: Appends a new row (start frame, end frame, label) to the CSV file.
- **Video Control Loop**: Handles video playback, pausing, and frame navigation.
- **Label Input Mode**: After marking start and end frames, the script switches to label input mode, allowing you to assign a numeric label to the selected section.

### Handling Frame Navigation

When the video is paused, you can step through individual frames using the `D` (or Right Arrow) and `A` (or Left Arrow) keys to precisely select the start and end points.

### Error Handling

- If the video fails to load, the script will print an error and exit.
- If invalid label input is provided, the script will prompt the user to input a valid label (between 1 and 60).

### Cleanup

When the script exits (by pressing `Q`), it will release the video file and close any open windows.

## Customization

- **Video Path**: Change the `video_file` variable to specify a different video file.
- **Label Range**: Modify the range check in the label input section to allow for different label values (Currently set to 1 to 70).
