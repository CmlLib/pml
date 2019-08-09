import mlogin
import mlaunchoption
import pml
import subprocess
import os


# initialize
#p = os.environ["appdata"] + "\\.minecraft"
p = os.getcwd() + "/game"
pml.initialize(p)
print("Initialized in " + pml.getGamePath())


# login
print("session : test user (tester123)")
session = mlogin.session()
session.username = "tester123"
session.uuid = "uuid"
session.access_token = "access_token"


# get profiles
profiles = pml.updateProfiles()
for item in profiles:
    print(item.name)

print("input version : ")
inputVersion = input()


# download event handler
def downloadEvent(x):
    print(x.filekind + " - " + x.filename + " - " + str(x.currentvalue) + "/" + str(x.maxvalue))


# launch option
option = mlaunchoption.launchoption()
option.maximumRamSizeMB = 4096
option.session = session


# download profile and create argument
pml.downloadEventHandler = downloadEvent
args = pml.startProfile(inputVersion, option)


# start process
with open("args.txt", "w") as f:
    f.write(args)

print(args)
mc = subprocess.Popen("java.exe " + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=pml.getGamePath())

print("launched!")

with mc.stdout as gameLog:
    while True:
        line = gameLog.readline()
        if not line:
            break
        print(line)

if mc.returncode:
    print(f"Client returned {mc.returncode}!")
