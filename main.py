from pmlauncher import pml, mlogin, mlaunchoption
import subprocess
import os


# initialize
# p = os.environ["appdata"] + "\\.minecraft"  # windows default game directory
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
# filekind : library , minecraft, index, resource
def downloadEvent(x):
    print(x.filekind + " - " + x.filename + " - " + str(x.currentvalue) + "/" + str(x.maxvalue))


pml.downloadEventHandler = downloadEvent

# launch option
option = mlaunchoption.launchoption()
option.maximumRamSizeMB = 4096
option.session = session
# option.screenWidth = 1600
# option.screenHeight = 900
# option.serverIp = "127.0.0.1"
# option.launcherName = "python_minecraft_launcher"
# option.customJavaParameter = "-Xms1024M"


# download profile and create argument
args = pml.startProfile(inputVersion, option)


# start process
with open("args.txt", "w") as f:  # for debug
    f.write(args)
print(args)

# in linux system, use os.system instead of subprocess
# os.system("java " + args)
mc = subprocess.Popen("java " + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=pml.getGamePath())

print("launched!")


# write output
with mc.stdout as gameLog:
    while True:
        line = gameLog.readline()
        if not line:
            break
        print(line)

if mc.returncode:
    print(f"Client returned {mc.returncode}!")
