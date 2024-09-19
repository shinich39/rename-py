import os
import csv
import re
import sys

def is_empty(str):
  return str == None or str == ""

def main(file_path):
  with open(file_path, "r") as file:
    reader = csv.reader(file)

    queue = []
    for row in reader:
      old_path = row[0]
      new_path = row[len(row) - 1]
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
    print(e)

