germanium master
================

_This is the optional drivers package._

Germanium is a set of extensions on top of the regular WebDriver API, allowing
for a super easy creation of tests. It's opensource and free.

```sh
pip install -U germanium[germaniumdrivers]
```

Simply put Germanium is a Web Testing API that doesn't disappoint.

```python
from germanium.static import *
from time import sleep

open_browser("ff")
go_to("http://www.google.com")
type_keys("germanium pypy<enter>", Input("q"))
wait(Link("Python Package Index"))
click(Link("Python Package Index"))
sleep(5)
close_browser()
```

Here is the [usage documentation](http://germaniumhq.com/documentation/), or as [PDF](http://germaniumhq.com/documentation/germanium-usage.pdf)

