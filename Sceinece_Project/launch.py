import os

array_width = [1920, 1280,  640]

for width in array_width:
    original_row_launch = 'python3 test.py ' + str(width)
    row_launch = 'python3 1OneBackground.py ' + str(width)
    row_launch2 = 'python3 2MeanBackground.py ' + str(width)
    row_launch3 = 'python3 3FilterBackground.py ' + str(width)

    os.system(original_row_launch)
    os.system(row_launch)
    os.system(row_launch2)
    os.system(row_launch3)