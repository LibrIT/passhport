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
CMD="${PADM} user"
USERNAME="thisis.a.test@with.name.org"
COMMENT="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed neque eget velit ultrices rhoncus nec at tellus. Sed efficitur lobortis erat, at faucibus sapien porttitor porta. Sed cursus, orci et ullamcorper rutrum, libero sapien ornare justo, at pellentesque eros magna sit amet risus. Nam consectetur cursus rutrum. Duis pretium nibh eu est condimentum, vitae ultrices felis suscipit. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Ut tristique posuere tempus. Suspendisse potenti. Curabitur dapibus leo erat, vitae vestibulum risus fermentum id. Donec semper ex augue, non hendrerit neque lacinia a."
SSHKEY="ssh-rsa AAAAB3NzaC1yc2TAAAADAQABAAABAQCoeJeOHb++y3dx6sv26/wHbWyX5sbtwKbabCovD3BUchUG3548CaxAk1N03sOo+/QFq/CpOLG/BeJ+/oZfmVKeuqfok6ZkS2BdU+UJYEJCYU/HCPEgfU81nQcsxnVJYvhquHQO4yHpyC/vcbkiY6Wm2vBW1QyQILtvT0RNybDGuvwsvG95Zk6oy2Kuja6giPA1Mu8YwOKK9MDGkaJCw9dMZKy2r5rpBe9XaZZfgz2Ll0jUmvLL41jk/y60o8blpP1coQw2QcGcLozCJLGyXZUJI9a6tvyLij56BLh7+G4Ji7jjV7CAGn5cwbvNKiqIgUTVJDavV4JbjnRbjZhm+oB5 ${USERNAME}"

#Tests
# Search/show/edit/del on a not existing user
# Creating user
# Creating an already existing user
# Search/show/edit/del an existing user

# SEARCH 1/2 
PATTERN="No user matching the pattern \"${USERNAME}\" found."
${CMD} search ${USERNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] search 1/2: " ${r/1/ERROR}

# SHOW 1/2
PATTERN="ERROR: No user with the name \"${USERNAME}\" in the database."
${CMD} show ${USERNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] show   1/2: " ${r/1/ERROR}

# EDIT 1/2
PATTERN="ERROR: No user with the name \"${USERNAME}\" in the database."
${CMD} edit ${USERNAME} --newname=new_${USERNAME} --newcomment="${COMMENT}" --newsshkey="${SSHKEY}" | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] edit   1/2: " ${r/1/ERROR}

# DEL 1/2
PATTERN="ERROR: No user with the name \"${USERNAME}\" in the database."
${CMD} delete ${USERNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] del    1/2: " ${r/1/ERROR}

# CREATE 1/2
PATTERN="OK: \"${USERNAME}\" -> created"
${CMD} create ${USERNAME} "${SSHKEY}" --comment="${COMMENT}" | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] create 1/2: " ${r/1/ERROR}

# CREATE 2/2
PATTERN="ERROR: The name \"${USERNAME}\" is already used by another user" 
${CMD} create ${USERNAME} "${SSHKEY}" --comment="${COMMENT}" | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] create 2/2: " ${r/1/ERROR}

# SEARCH 2/2
PATTERN="thisis.a.test@with.name.org"
${CMD} search ${USERNAME} | grep "${PATTERN}"  &> /dev/null
r=${?/0/OK}
echo "[user] search 2/2: " ${r/1/ERROR}

# SHOW 2/2
PATTERN="Name: ${USERNAME}
SSH key: ${SSHKEY}
Comment: ${COMMENT}"
${CMD} show ${USERNAME} | grep "${PATTERN}" | wc -l | grep 3 &> /dev/null
r=${?/0/OK}
echo "[user] show   2/2: " ${r/1/ERROR}

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
