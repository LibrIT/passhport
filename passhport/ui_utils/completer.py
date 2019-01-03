# -*-coding:Utf-8 -*-

"""Contains an object used to complete the targets names on the menu cli"""
import os
import sys
import readline
import glob

class tabCompleter(object):
    """ https://gist.github.com/iamatypeofwalrus/5637895 """

    def createListCompleter(self,ll):
        """ Since the autocomplete function can't be given a list to complete from
        a closure is used to create the listCompleter function with a list to complete
        from.
        """
        def listCompleter(text,state):
            line   = readline.get_line_buffer()

            if not line:
                return [c + " " for c in ll][state]

            else:
                return [c + " " for c in ll if c.startswith(line)][state]

        self.listCompleter = listCompleter
