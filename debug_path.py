import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"os.path.abspath('.'): {os.path.abspath('.')}")
print(f"os.path.abspath('..'): {os.path.abspath('..')}")
print(f"os.path.abspath('../..'): {os.path.abspath('../..')}")
print(f"sys.path: {sys.path}")
