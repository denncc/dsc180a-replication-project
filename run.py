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

if __name__ == "__main__":
    target = sys.argv[-1]
    main(target)
    