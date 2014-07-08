import sys
import time
def getWord(st):
    new_st = ''
    for s in st:
        if s == ' ':
            break
        new_st += s
    return new_st
def removeWord(st,word):
    st = st.replace(word,'',1)
    if len(st) > 1:
        st = st.replace(' ','',1)
    return st
def checkWord(word):
    if word == '':
        return ' '
    if len(word) == 2:
        if not (word[0] == '.' or word[1] == '.'):
            return word
    return '\n'
f = open('ourIBEO','r')
st = f.read()#.encode('hex')
new_st = ''
count  = 0
start_time = time.time()
elaps_time = time.time() - start_time
el_time = 10
while (len(st) > 20):
    s = getWord(st)
    st = removeWord(st,s)
    word = checkWord(s)
    new_st += word + ' '
    count += 1
    elaps_time = time.time() - start_time
    if elaps_time > el_time:
        print "took ", len(new_st),' bytes. '
        inp = input( 'Continue converting?')
        if inp == 0:
            break
        else:
            el_time = inp
            start_time = time.time()
            elaps_time = time.time() - start_time

print elaps_time , " length of new file is ", len(new_st), ' bytes'
file = open("ourIBEOclean.txt", "w")
file.write(new_st)
file.close()
