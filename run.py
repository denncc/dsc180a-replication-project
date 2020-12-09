import os
import json
import sys

# data module is used to retrieve data and process it using the pipeline
import src.data.make_dataset as dm
import src.features.build_features as bf

def main(target):
    if target == "run.py":
        dm.main()
        print("run the whole project")
    elif target == "test":
        # dm.test()
        # print("finished running on the test target")
        print("start testing on feature generating\n")
        bf.test_r()
        print("\nfinish testing on feature generating")

    elif target == "check":
        print("start performing checking on the processed data")
        dm.check()
        print("checking process has been performed")

if __name__ == "__main__":
    target = sys.argv[-1]
    main(target)
    