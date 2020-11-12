from germanium.static import *
from time import sleep

open_browser("ff")
go_to("http://www.google.com")
type_keys("germanium pypi<enter>", Input("q"))
wait(S(Link("Python Package Index")))
click(Link("Python Package Index"))
sleep(5)
close_browser()
