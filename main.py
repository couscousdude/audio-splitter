from pydub import AudioSegment
import os

def format_file_name(fileName):
    return "_".join(fileName.split(" ")).lower()

# converts timestamp in format mm:ss to seconds
def mm_ss_2_s(time_string):
    components = time_string.split(":")
    return int(components[0]) * 60 + int(components[1])

def split_audio(input_path, timestamps_dict):
    # Extract the base name of the input file (without extension)
    base_name = format_file_name(os.path.splitext(os.path.basename(input_path))[0])

    try:
        # Create 'output' directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create a subdirectory for this specific audio file
        file_output_dir = os.path.join(output_dir, base_name)
        if not os.path.exists(file_output_dir):
            os.makedirs(file_output_dir)
    except OSError as e:
        print(f"Error creating output directory: {e}")

    try:
        audio = AudioSegment.from_file(input_path)
    except FileNotFoundError:
        print(f"File not found: {input_path}")
        return
    
    output_format='m4a'

    for tag, timestamps in timestamps_dict.items():
        # Convert mm:ss timestamps to seconds
        if (type(timestamps[0]) == str):
            timestamps = [mm_ss_2_s(timestamps[0]), timestamps[1]]
        if (type(timestamps[1]) == str):
            timestamps = [timestamps[0], mm_ss_2_s(timestamps[1])]

        start_time, end_time = timestamps
        start_time_ms = start_time * 1000
        end_time_ms = end_time * 1000

        try:
            extracted_audio = audio[start_time_ms:end_time_ms]
        except ValueError:
            print(f"Error extracting audio: {input_path}")
            return

        output_file_name = f"{format_file_name(tag)}.{output_format}"
        output_file_path = os.path.join(file_output_dir, output_file_name)

        # Specify codec for m4a format
        extracted_audio.export(output_file_path, format="ipod", codec="aac")
        print(f"Exported '{output_file_name}'")

# Example usage
# Timestamps can be specified in seconds (int) or in minutes:seconds (string)
timestamps_dict = {
    "Part 1": [0, 30],
    "Part 2": [30, "2:00"],
    "Part 3": ["2:00", "3:40"]
}

split_audio("files/sample_audio.m4a", timestamps_dict)
