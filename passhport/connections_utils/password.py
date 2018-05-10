# -*-coding:Utf-8 -*-

"""Contains functions to manage passwords changes"""
import os, random, crypt, requests, configparser

conf = configparser.ConfigParser()
conffile = "passhport.ini"
if os.path.isfile("/etc/passhport/" + conffile):
    conf.read("/etc/passhport/" + conffile)
else:
    conf.read(sys.path[0] + "/" + conffile)

# SSL Configuration
SSL                = conf.getboolean("SSL", "SSL")
SSL_CERTIFICAT     = conf.get("SSL", "SSL_CERTIFICAT")

def generate():
    """ Generate a random password
        interactivepython.org
        /runestone/static/everyday/2013/01/3_password.html """
    alphabet = "abcdefghijklmnopqrstuvwxyz.&(-_)#{[]}@=+"
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    upperalphabet = alphabet.upper()
    pw_len = 16
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


def reset(tname, server, login, sshoptions, port, isodate):
    """After a session, we reset the user password
       and store the password in a local file"""
    # 1. Generate random passowrd
    pwdstring = generate()

    # 2. Define username (if passed in sshoptions it's used instead of login)
    useroption = sshoptions.split("-l")[-1].split(' ')
    if len(useroption) > 0  and useroption[0]:
            user = useroption[0]
    elif len(useroption) > 1 and useroption[1]:
            user = useroption[1]
    else:          
        user = login

    # 3. Propage password (this command HAS to be launched as root)
    r = os.popen("ssh -q -o BatchMode=yes root@" + server + ' ' + sshoptions + \
              ' -p ' + str(port) + ' -l root \'echo "' + \
              user + ':' + pwdstring + '" | chpasswd\' ' +\
              '&& echo -n changed').read()

    # 4. Sore it if it has been changed
    if r == "changed":

        """Send request to the passhportd """
        url = "http" + conf.getboolean("SSL", "SSL")*"s" + \
                    "://" + conf.get("Network", "PASSHPORTD_HOSTNAME") + \
                    ":" + conf.get("Network", "PORT") + "/"
        url = url + "target/savepassword"
        data= {"connectiondate" : isodate,
               "target"         : tname,
	       "password"       : pwdstring}

        try:
            if SSL:
                r = requests.post(url, data = data, verify=SSL_CERTIFICAT)
            else:
                r = requests.post(url, data = data)

        except requests.RequestException as e:
            print("ERROR: " + str(e.message))
        else:
            if r.status_code == requests.codes.ok:
                return r.text
        return 1
