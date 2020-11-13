RobotFramework bindings for Germanium.

Installation
============

.. code:: sh

    pip install robotframework-germaniumlibrary

Keyword List
============

-  use selenium browser

-  open browser

-  close browser

-  maximize window

-  click

-  double click

-  hover

-  right click

-  go to

-  type keys

-  type keys in

-  drag and drop

-  select by index

-  select by text

-  select by value

-  deselect by index

-  deselect by text

-  deselect by value

-  select file

-  assert exists

-  assert missing

Sample Standalone Usage (recommended)
=====================================

.. code:: robotframework

    *** Settings ***
    Library  GermaniumLibrary

    *** Test Cases ***
    This is a simple test case
        Open Browser  chrome
        Maximize Window
        Go To  https://germaniumhq.com
        Click  Link("Log In")
        Assert Exists  Input().right_of(Text("Email"))
        Type Keys In  Input().right_of(Text("Email"))  someuser
        Close Browser

Usage With SeleniumLibrary
==========================

To use the browser from selenium, instruct Germanium to use it *after*
you instantiate it using the ``Use Selenium Browser`` keyword.

.. code:: robotframework

    *** Settings ***
    Library  SeleniumLibrary
    Library  GermaniumLibrary

    *** Test Cases ***
    This is a test case to show usage with the SeleniumLibrary
        SeleniumLibrary.Open Browser  https://germaniumhq.com  chrome
        GermaniumLibrary.Use Selenium Browser
        GermaniumLibrary.Maximize Window
        GermaniumLibrary.Click  Link("Log In")
        GermaniumLibrary.Type Keys In  Input().right_of(Text("Email"))  someuser
        GermaniumLibrary.Assert Exists  Input()
        GermaniumLibrary.Assert Missing  Text("eeee")
        SeleniumLibrary.Close Browser
