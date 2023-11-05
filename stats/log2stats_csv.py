from engine_libs.log_lib import *

import re, os, sys
from datetime import datetime, timedelta

def read_logfile_lines(log_file_path, log_file_name):
  log_file = os.path.join(log_file_path, log_file_name)
  with open(log_file, 'r') as log_file:
    for line in log_file:
        match = re.match(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.(?P<milliseconds>\d{1,3})\.(?P<microseconds>\d{6}) \[INFO\]: (?P<message>.*)', line)
        if match:
            timestamp = match.group('timestamp')
            milliseconds = match.group('milliseconds').rjust(3, '0')
            microseconds = match.group('microseconds')
            message = match.group('message')
            
            full_timestamp = f'{timestamp}.{milliseconds}{microseconds[0:3]}'

            # Convert the full timestamp to a Python datetime object
            timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
            full_timestamp = full_timestamp.ljust(26, '0')  # Ensure microseconds are always 6 digits
            python_timestamp = datetime.strptime(full_timestamp, timestamp_format)
            
            # Now you can use the full_timestamp and message as needed
            yield python_timestamp, message 
        else:
            raise Exception(f'Skipping line: {line.strip()}')

def analyse_message(message):
  parts = re.split(r'[;:]', message)
  type = parts[0]
  if type == "Black to move":
    return "", "", ""
  try:
    op_index = str(list(LOG_OP_TYPES).index(parts[1]))
    op = parts[1]
  except ValueError:
    op = ""
  param_values = ""
  for _, param in enumerate(LOG_PARAMS):
    try:
      part_index = parts.index(param)
      param_values+= str(parts[part_index + 1]) + ";"
    except ValueError:
      param_values += ";"
  return type, op, param_values

def convert_log_file(file_path, file_name, max = sys.maxsize):
  outputfile = file_name.replace(".log", ".csv")
  with open(os.path.join(file_path, outputfile), mode="w", newline="") as file:
    file.write(get_header())
    for timestamp, message in read_logfile_lines(file_path, file_name):
      if timestamp and message:
          type, op, param_values = analyse_message(message)
          if type != "":
            file.write(str(timestamp) + ";" + type + ";" + op + ";" + param_values + "\n")
      else:
          raise Exception(f'Wrong Format')

      max -= 1
      if max <= 0:
        break
      
if __name__ == "__main__":
    convert_log_file("/Volumes/T1_Mini/Engine_Logs/", "fischer.log")