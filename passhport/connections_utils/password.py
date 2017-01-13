# -*-coding:Utf-8 -*-

"""Contains functions to manage passwords changes"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, random, crypt

def generate():
    """ Generate a random password
        interactivepython.org
        /runestone/static/everyday/2013/01/3_password.html """
    alphabet = "abcdefghijklmnopqrstuvwxyz.&(-_)#{[]}@=+"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    upperalphabet = alphabet.upper()
    pw_len = 12
    pwlist = []
    
    for i in range(pw_len//3):
        pwlist.append(alphabet[random.randrange(len(alphabet))])
        pwlist.append(upperalphabet[random.randrange(len(upperalphabet))])
        pwlist.append(str(random.randrange(10)))

    for i in range(pw_len-len(pwlist)):
        pwlist.append(alphabet[random.randrange(len(alphabet))])

    random.shuffle(pwlist)
    pwstring = "".join(pwlist)

    return pwstring


def reset(server, login, sshoptions):
    """After a session, we reset the user password
       and store the password in a local file"""
    # 1. Generate random passowrd
    pwdstring = generate()

    # 2. Define username (if passed in sshoptions it's used instead of login)
    useroption = sshoptions.split("-l")[-1].split(' ')
    if useroption[0]:
        user = useroption[0]
    elif useroption[1]:
        user = useroption[1]
    else:          
        user = login

    # 3. Propage password (this command HAS to be launched as root)
    os.system("ssh root@" + server + ' ' + sshoptions + ' -l root \'echo "'
                + user + ':' + pwdstring + '" | chpasswd\'')

    # 4. Sore it locally
    if not os.path.exists(PWD_FILE_DIR):
        os.mkdir(PWD_FILE_DIR)

    file = open(PWD_FILE_DIR + '/' + server + "_" + user, 'w')
    file.write(user + " : " + pwdstring)
    file.close()

