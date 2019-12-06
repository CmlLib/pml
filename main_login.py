from pmlauncher import pml, mlogin, mlaunchoption
import subprocess
import os
import sys


# initialize
# p = os.environ["appdata"] + "\\.minecraft"  # windows default game directory
p = os.getcwd() + "/game"
#p = os.path.abspath("/home/myu/.minecraft")
pml.initialize(p)
print("Initialized in " + pml.getGamePath())


# online-mode login (need pycraft : https://github.com/ammaraskar/pyCraft)
# download pyCraft and copy 'minecraft' directory to 'pycraft' directory.
from pycraft import authentication

mcid = input("input mojang email : ")
mcpw = input("input mojang pw : ")

auth = authentication.AuthenticationToken()
auth.authenticate(mcid, mcpw)  # input mojang email and password

session = mlogin.session()  # set session object
session.username = auth.profile.name
session.uuid = auth.profile.id_
session.access_token = auth.access_token

print("login success : " + session.username)


# get profiles
profiles = pml.updateProfiles()
for item in profiles:
    print(item.name)

inputVersion = input("input version : ")


# download event handler
# filekind : library , minecraft, index, resource
def downloadEvent(x):
    print(x.filekind + " - " + x.filename + " - " + str(x.currentvalue) + "/" + str(x.maxvalue))


pml.downloadEventHandler = downloadEvent

# download profile and create argument
args = pml.startProfile(inputVersion, 
                        xmx_mb=1024,
                        session=session,

                        launcher_name="pml",  # option
                        server_ip="",
                        jvm_args="",
                        screen_width=0,
                        screen_height=0)


# start process
with open("args.txt", "w") as f:  # for debug
    f.write(args)
print(args)

mc = subprocess.Popen("java " + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=pml.getGamePath(), shell=True)

print("launched!")


# write output
with mc.stdout as gameLog:
    while True:
        try:
            line = gameLog.readline()
            if not line:
                break
            print(line.decode(sys.getdefaultencoding()))
        except:
            pass

if mc.returncode:
    print(f"Client returned {mc.returncode}!")

