import re
import sys
import pandas as pd

def extract_data(log_file, num_cores):
    # Regular expressions to extract relevant information from the log file
    run_pattern = re.compile(r"Run (\d+):")
    usr_pattern = re.compile(r"(\d+\.\d+)user")
    sys_pattern = re.compile(r"(\d+\.\d+)system")
    real_pattern = re.compile(r"(\d+:\d+\.\d+)elapsed")

    # Initialize variables to store extracted values
    run_no = None
    usr_time = None
    sys_time = None
    real_time = None

    # Create an empty list to store the extracted data
    data = []

    # Open and read the log file
    with open(log_file, 'r') as file:
        lines = file.readlines()

    # Parse the log file and extract the data
    for line in lines:
        run_match = run_pattern.search(line)
        if run_match:
            run_no = int(run_match.group(1))

        usr_match = usr_pattern.search(line)
        if usr_match:
            usr_time = float(usr_match.group(1))

        sys_match = sys_pattern.search(line)
        if sys_match:
            sys_time = float(sys_match.group(1))

        real_match = real_pattern.search(line)
        if real_match:
            real_time = real_match.group(1)

            # Append the data to the list
            data.append({"Num Cores": num_cores, "Run No.": run_no, "usr (s)": usr_time, "system (s)": sys_time, "total (s)": real_time})

    return data

def main(log_files, output_file):

    data = []

    for log_file, num_cores in log_files:
        extracted_data = extract_data(log_file, num_cores)
        data.extend(extracted_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Function to convert time to seconds
    def convert_time_to_seconds(time_str):
        try:
            minutes, rest = time_str.split(':')
            seconds, milliseconds = rest.split('.')
            return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
        except (ValueError, AttributeError):
            # Handle cases where the value is not in the expected format (e.g., float)
            return 0 # or any appropriate default value

    # Apply the conversion function to the "total" column
    df['total (s)'] = df['total (s)'].apply(convert_time_to_seconds)

    # Create a new DataFrame for averages
    averages = df.groupby('Num Cores').agg({'usr (s)': 'mean', 'system (s)': 'mean', 'total (s)': 'mean'}).reset_index()

    # Merge the averages DataFrame back into the original DataFrame
    df = df.merge(averages, on='Num Cores',  suffixes=('', '_avg'))

    # Save the data to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4 or (len(sys.argv) - 2) % 2 != 0:
        print("Usage: python script.py output_file log_file1 num_cores1 [log_file2 num_cores2 ...]")
    else:
        output_file = sys.argv[1]
        log_files = [(sys.argv[i], int(sys.argv[i+1])) for i in range(2, len(sys.argv), 2)]
        main(log_files, output_file)
