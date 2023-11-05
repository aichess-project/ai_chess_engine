import os, csv
from engine_libs.log_lib import *
from datetime import datetime

def amend_timestamps(df):
    for row in df.iterrows():
        if len(df["Timestamp"] == 19):  # Check if the timestamp has the format 'YYYY-MM-DD HH:MM:SS'
            print(row)
            df["Timestamp"] += ".000000"
    
def read_csv(file_path, file_name):
   
    file = os.path.join(file_path, file_name)


    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if "ALPHA_BETA_BREAK" in row:
                yield row["Timestamp"], row["Type"], row["Op"], row["ALPHA_BETA_BREAK"]
            else:
                yield row["Timestamp"], row["Type"], row["Op"], False

def get_op_index(op):
    try:
        return LOG_OP_TYPES.index(op)
    except ValueError:
        print(f"{op} is not in the list")
        return None

def create_stat_files(file_path):
    file_list = []
    for op in LOG_OP_TYPES:
        filename = "stat" + "-" + op + ".csv"
        try:
            file = open(os.path.join(file_path, filename), mode="w", newline="")
            writer = csv.writer(file)
            file_list.append(writer)
        except Exception as e:
            print(f"An error occurred: {e}")
    return file_list

timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
timestamp_format_alternative = '%Y-%m-%d %H:%M:%S'

def str2ts(str):
    try:
        return datetime.strptime(str, timestamp_format)
    except Exception as e:
        try:
            return datetime.strptime(str, timestamp_format_alternative)
        except Exception as e:
            print(f"A conversion error occurred: {e} \n {str}")

def get_delta_seconds(duration):
    return duration.total_seconds()

def create_stats(file_path, file_name, file_list):
    time_stamps = {}
    for index, _ in enumerate(LOG_OP_TYPES):
        time_stamps[index] = None
    nr_nodes = 0
    nr_ab_breaks = 0

    for timestamp, type, op, ab_break in read_csv(file_path, file_name):
        if op == "" or op is None:
            continue
        if type in [get_start_string(), get_end_string()]:
            op_index = get_op_index(op)
            if type == get_start_string():
                time_stamps[op_index] = str2ts(timestamp)
                if op == OP_EXT_EVAL:
                    nr_nodes += 1
            else:
                if time_stamps[op_index] is not None:
                    end = str2ts(timestamp)
                    data_to_write = [time_stamps[op_index], end, end - time_stamps[op_index], get_delta_seconds(end - time_stamps[op_index])]
                    if op == OP_FIND_BEST:
                        data_to_write.append(nr_nodes)
                        data_to_write.append(nr_ab_breaks)
                        nr_nodes = 0
                        nr_ab_breaks = 0
                    elif op == OP_ALPHABETA and ab_break:
                        nr_ab_breaks += 1
                    try:
                        file_list[op_index].writerow(data_to_write)
                    except Exception as e:
                        print(f"A fileIO error occurred: {e} \n {str} {type} {op} {op_index}")
                        return

                    time_stamps[op_index] = None
                else:
                    pass
                    #print(f"Error {timestamp} {op}")

if __name__ == "__main__":
    filepath = "/Volumes/T1_Mini/Engine_Logs/"
    file_name = "fischer.csv"
    filepath = "/Volumes/T1_Mini/Engine_Logs/MiniMax1"
    file_name = "engine.csv"
    file_list = create_stat_files(filepath)
    create_stats(filepath, file_name, file_list)
    