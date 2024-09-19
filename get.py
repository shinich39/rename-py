import os
import sys
import csv
import re
import pathlib

extension_list = (".jpg", ".jpeg", ".png", ".tif", ".tiff")
path_regex = r'[\\\/]+'
path_pad_left = False
name_regex = r'[-_\s]+'
name_pad_left = False

def filter(str):
  # filename, extension = os.path.splitext(str)

  if str.lower().endswith(extension_list) == False:
    return False

  return True

def get_files(root):
  result = []
  for path, subdirs, files in os.walk(root):
    for name in files:
      file_path = os.path.join(path, name)
      if re.search(r'__pycache__', file_path):
        continue
      file_path = re.sub(r'^\.[\\\/]+', "", file_path)
      result.append(file_path)
  return result

def filter_files(files):
  result = []
  for p in files:
    if filter(p):
      result.append(p)
  return result

def split_files(files):
  path_list = []
  path_parts_list = []
  name_parts_list = []
  for file_path in files:
    file_path = re.sub(path_regex, "/", file_path)

    path_parts = re.split(path_regex, file_path)

    path = pathlib.Path(file_path)
    filename, extension = os.path.splitext(path.name)
    name_parts = re.split(name_regex, filename)
    name_parts.append(extension)

    path_list.append(file_path)
    path_parts_list.append(path_parts)
    name_parts_list.append(name_parts)

  return (path_list, path_parts_list, name_parts_list)

def get_max_length(l):
  size = 0
  for a in l:
    if len(a) > size:
      size = len(a)
  return size

def add_pad(lists, size, pad_left):
  for l in lists:
    while len(l) < size:
      if pad_left:
        l.insert(0, "")
      else:
        l.append("")

def add_delimeter(files):
  for arr in files:
    for i, v in enumerate(arr):
      arr[i] = f'"{v}"'
      
def main(root):
  files = get_files(root)
  files = filter_files(files)

  # path => (paths, path_parts, name-parts)
  files, path_parts, name_parts = split_files(files)

  add_pad(path_parts, get_max_length(path_parts), path_pad_left)
  add_pad(name_parts, get_max_length(name_parts), name_pad_left)

  # join
  data = []
  for i in range(len(files)):
    data.append([files[i], "=>", *path_parts[i], "=>", *name_parts[i], "=>", files[i]])

  # debug
  print(">", f"Load {len(data)} files.")
  for d in data:
    print(">", d[0])

  # write
  with open("./result.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

  print(">", f"result.csv created.")

if __name__ == "__main__":

  args = sys.argv[1:]
  if len(args) == 0 or args[0] == None or args[0] == "":
    args.insert(0, ".")

  root = os.path.relpath(args[0], ".")
  print(">", f"Set directory to \"{root}\"")

  main(root)