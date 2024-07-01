# HFSSToolBox
A useful toolbox for HFSS

## Before runnig
Download all the files and put them in a **folder**

Change the config file path in MainForm.py (line 75) into your **folder** before your first time running

It looks like:

```python
f = open("yourpath/Toolbox.config",'r')
```

For example:

```python
f = open("C:/Users/username/Desktop/HFSSToolBox/Toolbox.config",'r')
```

**Note: use '/' instead of  '\\' , or HFSS will report an error!**

And also edit the path in Program.py (line 8) 

It looks like:

```python
sys.path.append(r"your path")
```

For example:

```python
sys.path.append(r"C:\Users\username\Desktop\HFSSToolBox")
```

## How to run

Open your HFSS and run it by using menu: Tools -> Run Script

Select Program.py and run

You can also add it to your custom tools
