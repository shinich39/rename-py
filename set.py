import os
import csv
import re
import sys
import pathlib

def is_empty(str):
  return str == None or str == ""

def get_dirname(str):
  return os.path.dirname(str)

def get_filename(str):
  path = pathlib.Path(str)
  return path.stem

def get_extension(str):
  return os.path.splitext(str)[1]

def main(file_path):
  with open(file_path, "r") as file:
    reader = csv.reader(file)

    queue = []
    for row in reader:
      old_path = row[0]
      new_name = row[len(row) - 1] 
      dir_name = get_dirname(old_path)
      extension = get_extension(old_path)
      new_path = dir_name + "/" + new_name + extension

      if is_empty(old_path):
        raise Exception(f"{old_path} is not valid value")
      
      if os.path.exists(old_path) == False:
        raise Exception(f"{old_path} is not exists")
      
      if is_empty(new_path):
        raise Exception(f"{new_path} is not valid value")
      
      queue.append((old_path, new_path))
    
    change_count = 0
    for old_path, new_path in queue:
      
      if old_path == new_path:
        print(">", f"{old_path} is not changed")
        continue

      os.rename(old_path, new_path)
      print(">", old_path, "=>", new_path)
      change_count += 1

    print(">", f"{change_count} files changed")

if __name__ == "__main__":
  try:
    args = sys.argv[1:]
    if len(args) == 0 or is_empty(args[0]):
      if os.path.exists("./result.csv"):
        args.insert(0, "./result.csv")
      else:
        raise Exception("Argument must be a string")

    file_path = os.path.abspath(args[0])

    if os.path.exists(file_path) == False:
      raise Exception(f"{file_path} is not exists")
    
    if file_path.endswith(".csv") == False:
      raise Exception(f"{file_path} is not CSV file")
    
    print(">", "CSV:", file_path)

    main(file_path)
  except Exception as e:
    print("> Error:", e)

