import os
import csv

dirName = '/home/josh/google_drive/misc/foo/things/'
for i in os.listdir('/home/josh/google_drive/misc/foo/things/'):
    with open(dirName+i) as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        r = csv.reader(f, dialect)
        for row in r:
            print(row)
