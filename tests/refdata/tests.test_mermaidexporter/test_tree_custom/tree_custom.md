```mermaid
graph TD
%% just an example comment
%% could be an option too
N0("root")
N1("sub0")
N2("sub0B")
N3("sub0A")
N4("sub1")
N5("sub1A")
N6("sub1"B")
N7("su\b1C")
N8("sub1Ca")
N0--2-->N1
N0---->N4
N1--109-->N2
N1---->N3
N4--7-->N5
N4--8-->N6
N4--22-->N7
N7--42-->N8
```