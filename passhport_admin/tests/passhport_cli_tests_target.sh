#!/bin/bash
# Launch all command line which don't need interractions
# Goal is to be able to test rapidly all the passhport-admin
# basic functions

#GENERAL
PADM="/home/passhport/passhport-run-env/bin/python3 ./passhport-admin"

#################
# USER MANAGEMENT
#################
#Variables
CMD="${PADM} target"
LOGIN="MyLogin"
TARGETNAME="Mytarget"
HOSTNAME="Myhostname"
SSHOPTIONS="-x"
PORT="2222"
COMMENT="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed neque eget velit ultrices rhoncus nec at tellus. Sed efficitur lobortis erat, at faucibus sapien porttitor porta. Sed cursus, orci et ullamcorper rutrum, libero sapien ornare justo, at pellentesque eros magna sit amet risus. Nam consectetur cursus rutrum. Duis pretium nibh eu est condimentum, vitae ultrices felis suscipit. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."
SSHKEY="ssh-rsa AAAAB3NzaC1yc2TAAAADAQABAAABAQCoeJeOHb++y3dx6sv26/wHbWyX5sbtwKbabCovD3BUchUG3548CaxAk1N03sOo+/QFq/CpOLG/BeJ+/oZfmVKeuqfok6ZkS2BdU+UJYEJCYU/HCPEgfU81nQcsxnVJYvhquHQO4yHpyC/vcbkiY6Wm2vBW1QyQILtvT0RNybDGuvwsvG95Zk6oy2Kuja6giPA1Mu8YwOKK9MDGkaJCw9dMZKy2r5rpBe9XaZZfgz2Ll0jUmvLL41jk/y60o8blpP1coQw2QcGcLozCJLGyXZUJI9a6tvyLij56BLh7+G4Ji7jjV7CAGn5cwbvNKiqIgUTVJDavV4JbjnRbjZhm+oB5 ${USERNAME}"

#Tests
# Search/show/edit/del/adduser/rmuser on a not existing target
# Creating target
# Creating an already existing target
# Search/show an existing target
# Adduser 
# Show target with  users in it
# rmuser
# Show target without any user in it
# Edit target 
# delete target

# LIST 1/2
PATTERN="No target in database."
${CMD} list | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] list    1/2: " ${r/1/ERROR}

# SEARCH 1/2 
PATTERN="No target matching the pattern \"${TARGETNAME}\" found."
${CMD} search ${TARGETNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] search  1/2: " ${r/1/ERROR}

# SHOW 1/2
PATTERN="ERROR: No target with the name \"${TARGETNAME}\" in the database."
${CMD} show ${TARGETNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] show    1/2: " ${r/1/ERROR}

# EDIT 1/2
PATTERN="ERROR: No target with the name \"${TARGETNAME}\" in the database."
${CMD} edit ${TARGETNAME} --newname=new_${TARGETNAME} --newhostname=new_${HOSTNAME} --newcomment="new_${COMMENT}" --newsshoptions=new_${OPTIONS} --newport=new_${PORT} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] edit    1/2: " ${r/1/ERROR}

# DELETE 1/2
PATTERN="ERROR: No target with the name \"${TARGETNAME}\" in the database."
${CMD} delete -f ${TARGETNAME}  | grep "${PATTERN}" &> /dev/null
r=${?/0/OK}
echo "[target] delete  1/2: " ${r/1/ERROR}

# CREATE 1/2
PATTERN="OK: \"${TARGETNAME}\" -> created"
${CMD} create ${TARGETNAME} ${HOSTNAME}  --comment="${COMMENT}" --login="${LOGIN}" --sshoptions="${SSHOPTIONS}" --port="${PORT}" | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] create  1/2: " ${r/1/ERROR}

# CREATE 2/2
PATTERN="ERROR: The name \"${TARGETNAME}\" is already used by another target" 
${CMD} create ${TARGETNAME} ${HOSTNAME}  --comment="${COMMENT}" --sshoptions="${SSHOPTIONS}" --port="${PORT}" | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] create  2/2: " ${r/1/ERROR}

# SEARCH 2/2
PATTERN="${TARGETNAME}"
${CMD} search ${TARGETNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] search  2/2: " ${r/1/ERROR}

# SHOW 2/2
PATTERN="Name: ${TARGETNAME}
Hostname: ${HOSTNAME}
Login: ${LOGIN}
Port: ${PORT}
SSH options: ${OPTIONS}
Comment: ${COMMENT}
Attached users:
Usergroup list:
Users who can access this target:
All usergroups:
Member of the following targetgroups:"
${CMD} show ${TARGETNAME} | head -7 | grep "${PATTERN}" | wc -l | grep 7 &> /dev/null
r=${?/0/OK}
echo "[target] show    2/2: " ${r/1/ERROR}

# EDIT 2/2
PATTERN="OK: \"${TARGETNAME}\" -> edited" 
${CMD} edit ${TARGETNAME} --newname=new_${TARGETNAME} --newcomment="new_${COMMENT}" | grep "${PATTERN}" &> /dev/null
r=${?/0/OK}
echo "[target] edit    2/2: " ${r/1/ERROR}

# DEL 2/2
PATTERN="OK: \"new_${TARGETNAME}\" -> deleted"
${CMD} delete new_${TARGETNAME} -f | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] del     2/2: " ${r/1/ERROR}
