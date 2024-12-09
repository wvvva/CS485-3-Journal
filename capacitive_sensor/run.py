import subprocess
import time
import serial
from multiprocessing import Process, Value

# Path to the video file
video_path = "/Users/VanessaWei/Desktop/simple_cap_sensor-public/capacitive_sensor/video.mp4"

# Serial connection
ser = serial.Serial('/dev/tty.usbserial-A10LT13X', 9600)

def play_video(command, is_running):
    """
    Plays the video based on the command provided. Stops when `is_running` is set to False.
    """
    while is_running.value:
        if command == "play_video_1":
            start = 0
            length = 20  # Play first 22 seconds
        elif command == "play_video_2":
            start = 22
            length = 44  # Play from 22 to 44 seconds
        else:
            break

        # Start playing the new video section
        play_script = f'''
        tell application "QuickTime Player"
            set the current time of document 1 to {start}
            play document 1
        end tell
        '''
        subprocess.run(["osascript", "-e", play_script])

        # Wait for the duration of the segment
        time.sleep(length)

        # Pause playback to reset for next loop
        pause_script = '''
        tell application "QuickTime Player"
            pause document 1
        end tell
        '''
        subprocess.run(["osascript", "-e", pause_script])

        # Sleep briefly before potentially restarting the loop
        time.sleep(0.1)

def monitor_serial(is_running):
    """
    Monitors the serial port for commands and starts/stops the video playback process accordingly.
    """
    current_command = None
    video_process = None

    while True:
        if ser.in_waiting > 0:
            # Read and decode the serial command
            command = ser.readline().decode().strip()

            if command in ["play_video_1", "play_video_2"]:
                print(command)
                # If a new command is detected, stop the current process and start a new one
                if current_command != command:
                    # Stop the existing video process
                    if video_process is not None:
                        is_running.value = False
                        pause_script = '''
                        tell application "QuickTime Player"
                            pause document 1
                        end tell
                        '''
                        subprocess.run(["osascript", "-e", pause_script])
                        video_process.terminate()

                    # Start a new video process
                    is_running.value = True
                    print("start")
                    video_process = Process(target=play_video, args=(command, is_running))
                    video_process.start()
                    print("passed")

                    # Update the current command
                    current_command = command

        # Short sleep to reduce CPU usage
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        # Open the video file in QuickTime Player (once at the beginning)
        open_script = f'''
        tell application "QuickTime Player"
            open POSIX file "{video_path}"
        end tell
        '''
        subprocess.run(["osascript", "-e", open_script])

        # Shared variable to control video playback
        is_running = Value('b', False)  # Boolean flag for whether the video is playing

        # Start the serial monitoring process
        serial_process = Process(target=monitor_serial, args=(is_running,))
        serial_process.start()

        # Wait for the serial process to finish (won't happen unless interrupted)
        serial_process.join()

    except KeyboardInterrupt:
        # Quit QuickTime Player and clean up processes
        quit_script = '''
        tell application "QuickTime Player"
            quit
        end tell
        '''
        subprocess.run(["osascript", "-e", quit_script])
        print("Stopped playing and closed QuickTime Player.")
