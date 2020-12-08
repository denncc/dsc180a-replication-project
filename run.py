import os
import json
import sys

# data module is used to retrieve data and process it using the pipeline
import src.data.make_dataset as dm

def main(target):
    if target == "run.py":
        dm.main()
        print("run the whole project")
    elif target == "test":
        dm.test()
        print("finished running on the test target")
    elif target == "check":
        print("start performing checking on the processed dat")
        dm.check()
        print("checking process has been performed")

if __name__ == "__main__":
    target = sys.argv[-1]
    main(target)
    