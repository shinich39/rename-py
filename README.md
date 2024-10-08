# rename-py

Rename files in subdirectories by csv.  

## Requirements  

- [Python](https://www.python.org/)

## Usage  

Copy and paste get.bat, get.py, set.bat and set.py into the target directory.  

```console
py ./get.py
```

Edit end of row in result.csv  

```console
py ./set.py
```

## Functions  

- Join texts

```
=CONCAT(A1:A2)
```

- Add pad left

```
=CONCATENATE(REPT(0,2-LEN(A1)),A1)
```

- Remove all digits from text

```
=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A1,"0",""),"1",""),"2",""),"3",""),"4",""),"5",""),"6",""),"7",""),"8",""),"9","")
```

- Get text before character

```
=LEFT(A1, SEARCH("-", A1) - 1)
```

- Get digits from the beginning of text

```
=LEFT(A1, MATCH(0, ISNUMBER(MID(A1, ROW(INDIRECT("1:"&LEN(A1)+1)), 1) *1), 0) -1)
```

- Get digits from the end of text

```
=RIGHT(A1, LEN(A1) - MAX(IF(ISNUMBER(MID(A1, ROW(INDIRECT("1:"&LEN(A1))), 1) *1)=FALSE, ROW(INDIRECT("1:"&LEN(A1))), 0)))
```