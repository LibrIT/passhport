#!/usr/bin/env python
# -*-coding:Utf-8 -*-

def pcreate(param):
    """Prompt user to obtain data to request"""
    print "plop"


def create(param):
    """Format param for user creation"""
    comment = ""
    if '--comment' in param:
        comment = param['--comment']

    return {'name': param['<name>'], 
            'sshkey': param['<sshkey>'],
            'comment': comment}


def pedit(param):
    """Prompt user to obtain data to request"""
    print "1plop"


def edit(param):
    """Format param for user edition"""
    new_name = ""
    new_comment = ""
    new_sshkey = ""
    if '--newname' in param:
        new_name = param['--newname']
    if '--newcomment' in param:
        new_comment = param['--newcomment']
    if '--newsshkey' in param:
        new_sshkey = param['--newsshkey']

    return {'name': param["<name>"],
            'new_name': new_name,
            'new_comment': new_comment,
            'new_sshkey': new_sshkey}

