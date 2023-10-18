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

def main(log_file, output_file, num_cores):
    # Check if the log file exists
    try:
        with open(log_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"Error: The log file '{log_file}' does not exist.")
        return

    # Extract the data from the log file
    data = extract_data(log_file, num_cores)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Create a new Excel file or load the existing one
    try:
        existing_data = pd.read_excel(output_file)
        df = existing_data.append(df, ignore_index=True)
    except FileNotFoundError:
        pass

    # Save the data to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py log_file output_file num_cores")
    else:
        log_file = sys.argv[1]
        output_file = sys.argv[2]
        num_cores = int(sys.argv[3])
        main(log_file, output_file, num_cores)
