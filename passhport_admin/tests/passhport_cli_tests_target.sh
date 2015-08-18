#!/bin/bash
# Launch all command line which don't need interractions
# Goal is to be able to test rapidly all the passhport-admin
# basic functions

#GENERAL
PADM="./passhport-admin"

#################
# USER MANAGEMENT
#################
#Variables
CMD="${PADM} target"
TARGETNAME="Mytarget"
HOSTNAME="Myhostname"
SSHOPTIONS="-x"
PORT="2222"
COMMENT="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed neque eget velit ultrices rhoncus nec at tellus. Sed efficitur lobortis erat, at faucibus sapien porttitor porta. Sed cursus, orci et ullamcorper rutrum, libero sapien ornare justo, at pellentesque eros magna sit amet risus. Nam consectetur cursus rutrum. Duis pretium nibh eu est condimentum, vitae ultrices felis suscipit. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Ut tristique posuere tempus. Suspendisse potenti. Curabitur dapibus leo erat, vitae vestibulum risus fermentum id. Donec semper ex augue, non hendrerit neque lacinia a."
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
${CMD} delete -f ${TARGETNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[target] delete  1/2: " ${r/1/ERROR}

# CREATE 1/2
PATTERN="OK: \"${TARGETNAME}\" -> created"
${CMD} create ${TARGETNAME} ${HOSTNAME}  --comment="${COMMENT}" --sshoptions="${SSHOPTIONS}" --port="${PORT}" | grep "${PATTERN}"  &> /dev/null
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
PATTERN="Name: ${USERNAME}
SSH key: ${SSHKEY}
Port: ${PORT}
SSH options: ${SSHOPTIONS}
Comment: ${COMMENT}
User list:
Usergroup list:"
${CMD} show ${TARGETNAME} | grep "${PATTERN}" | wc -l | grep 7 &> /dev/null
r=${?/0/OK}
echo "[target] show   2/2: " ${r/1/ERROR}

# ADDUSER 1/2

# EDIT 2/2
PATTERN="OK: \"${USERNAME}\" -> edited" 
${CMD} edit ${USERNAME} --newname=new_${USERNAME} --newcomment="${COMMENT}" --newsshkey="${SSHKEY}" | grep "${PATTERN}" &> /dev/null
r=${?/0/OK}
echo "[user] edit   2/2: " ${r/1/ERROR}

# DEL 2/2
PATTERN="OK: \"new_${USERNAME}\" -> deleted"
${CMD} delete new_${USERNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] del    2/2: " ${r/1/ERROR}
