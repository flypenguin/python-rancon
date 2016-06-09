FROM python:3-onbuild

MAINTAINER Axel Bock <mr.axel.bock@gmail.com>

# Why-oh-why do I need to use abolute paths here?!? 
# (no, Docker 1.11.2 - relative paths didn't work).
# So if I read this next time, I will try, and it will work, and I will wonder,
# even though it's the same Docker version I bet, and seriously I hate it already.
# That's life in IT :D
ENTRYPOINT ["/usr/src/app/rancon.py"]

