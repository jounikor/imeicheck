#!/usr/bin/python

#
# (c) 2018 Jouni Korhonen (jouni.korhonen@iki.fi)
# 
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#

import sys
import argparse

# Check or generate Check Digit based on the first
# 14 or 15 characters on the inout line
def str2chksm( s ):
    """ str2chksm(s) -> int,int

    Keyword arguments:
    s -- string with first 14 or 15 characters being IMEI

    Description:
    If the input string first splitable string has 14 characters then
    generate the Check Digit for the IMEI code. Return id,None.
    If the input string first splitable string has 15 characters then
    verify the Check Digit of the IMEI. Return id,checksum.
    Otherwise, return None, None as an error.

    The input line can be anything as long as the first part has
    14 or 15 character IMEI. The rest of the line is ignored.

    """

    if s.__len__() > 14:
        cd = int(s[14])
    elif s.__len__() > 13:
        cd = None
    else:
        return None,None

    i = 13; mul = 2; sum = 0

    while i >= 0:
        n = int(s[i]) * mul

        if n >= 10:
            sum += ((n / 10) + (n % 10))
        else:
            sum += n

        mul ^= 3
        i -= 1

    id = sum % 10

    if id > 0:
        id = 10 - id

    return id,cd

#
# Usage:
#    python imei.py inputfile.txt 
#
if __name__ == "__main__":
    line = 0
    imei = 0
    
    prs = argparse.ArgumentParser()
    prs.add_argument("file",metavar="file",type=str,nargs=1,help="IMEI test file")
    prs.add_argument("-s","--show",dest="show",action="store_true",help="show comments with IMEIs")
    args = prs.parse_args()

    with open(args.file[0]) as fp:
        txt = fp.readline()
        while txt:
            # extract the first splitable string from the input line
            s = txt.split()
            
            if s.__len__() > 0:
                s = s[0].strip()
            else:
                s = None

            if s and s.isdigit() is False:
                if args.show:
                    print "invalid IMEI '{:s}' on line {:d}".format(s,line)
            elif s:
                if s.__len__() > 15:
                    if args.show:
                        print "too long IMEI '{:s}' on line {:d}".format(s,line)
                else:
                    id,cd = str2chksm(s)

                    if id == None:
                        if args.show:
                            print "invalid IMEI '{:s}' on line {:d}".format(s,line)
                    elif cd == None:
                        imei += 1

                        if args.show:
                            print "{:14s}{:d} <- added check digit on line {:d}".format(s,id,line)
                        else:
                            print "{:14s}{:d}".format(s,id) 
                    else:
                        if id != cd:
                            if args.show:
                                print "{:15s} <- invalid check digit on line {:d} - should be {:d}".format(s,line,id)
                        else:
                            print s
                            imei += 1

            txt = fp.readline()
            line += 1

    print "Number of correct(ed) IMEIs is ",imei


