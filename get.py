import os
import sys
import csv
import re
import pathlib

# options

extension_list = (".jpg", ".jpeg", ".png", ".tif", ".tiff")
path_regex = r'[\\\/]+'
name_regex = r'[-_+=.:;\s]+|([0-9]+)'

path_pad_left = False
name_pad_left = False

def filter(str):
  # enable hidden filter
  if str.startswith(".") == True:
    return False

  # enable extension filter
  # if str.lower().endswith(extension_list) == False:
  #   return False
  
  # add more filters...
  # path = pathlib.Path(str)
  # filename = get_filename(str)
  # dirname = get_dirname(str)
  # extension = get_extension(str)

  return True

# methods

def get_dirname(str):
  return os.path.dirname(str)

def get_filename(str):
  path = pathlib.Path(str)
  return path.stem

def get_extension(str):
  return os.path.splitext(str)[1]

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
  name_list = []
  path_parts_list = []
  name_parts_list = []
  division_list = []
  path_parts_size_list = []

  prev_path = None
  for i, file_path in enumerate(files):
    if prev_path == None:
      prev_path = os.path.dirname(file_path)
    elif prev_path != os.path.dirname(file_path):
      prev_path = os.path.dirname(file_path)

      # Add division row
      division_list.append(i)

    file_path = re.sub(path_regex, "/", file_path)
    filename = get_filename(file_path)

    path_parts = re.split(path_regex, os.path.dirname(file_path))
    for j, part in enumerate(path_parts):
      path_parts[j] = re.split(name_regex, part)
      path_parts[j] = [x for x in path_parts[j] if x != None and x != ""]
      
      

    name_parts = re.split(name_regex, filename)
    name_parts = [x for x in name_parts if x != None and x != ""]

    path_list.append(file_path)
    name_list.append(filename)
    path_parts_list.append(path_parts)
    name_parts_list.append(name_parts)

  # split path parts
  path_parts_sizes = get_max_lengths(path_parts_list)
  for i, path_parts in enumerate(path_parts_list):
    for j, parts in enumerate(path_parts):
      size = path_parts_sizes[j]
      add_pad_to_list(parts, size, path_pad_left)

  for i, path_parts in enumerate(path_parts_list):
    path_parts_list[i] = flatten_lists(path_parts)
  # path_parts_list = flatten_lists(path_parts_list)

  return (path_list, name_list, path_parts_list, name_parts_list, division_list)

def get_max_length(l):
  size = 0
  for a in l:
    if len(a) > size:
      size = len(a)
  return size

def get_max_lengths(l):
  sizes = []
  for i, a in enumerate(l):
    for j, b in enumerate(a):
      if len(sizes) <= j:
        sizes.append(0)

      if sizes[j] < len(b):
        sizes[j] = len(b)
  return sizes
  

def add_pad_to_list(list, size, pad_left):
  while len(list) < size:
    if pad_left:
      list.insert(0, "")
    else:
      list.append("")

def add_pad_to_lists(lists, size, pad_left):
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
  
def flatten_lists(lists):
  r = []
  for i, l in enumerate(lists):
    if i > 0:
      r += ["=>"]
    r += l
  return r

def main(root):
  files = get_files(root)
  files = filter_files(files)

  # path => (paths, names, path_parts, name-parts)
  paths, names, path_parts, name_parts, divisions = split_files(files)

  add_pad_to_lists(path_parts, get_max_length(path_parts), path_pad_left)
  add_pad_to_lists(name_parts, get_max_length(name_parts), name_pad_left)

  # join
  data = []
  for i in range(len(paths)):
    data.append([paths[i], "=>", *path_parts[i], "=>", *name_parts[i], "=>", names[i]])

  # debug
  print(">", f"Load {len(data)} files.")
  for d in data:
    print(">", d[0])

  # add divisions
  divisions.reverse()
  for i in divisions:
    data.insert(i, [])

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