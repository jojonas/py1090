Using the library
=================


Running dump1090
----------------
py1090 should work with it right out of the box with `dump1090 <https://github.com/MalcolmRobb/dump1090>`_. Just make sure that the TCP BaseStation output port of dump1090 (usually 30003) matches the port chosen in the connection: ::

	dump1090.exe --net --net-sbs-port 30003

.. seealso::
	`Dump1090 - Planeplotter Wiki <http://planeplotter.pbworks.com/w/page/79995023/Dump1090>`_

Running RTL1090
---------------
To work with py1090, the BaseStation output has to be activated inside of `RTL1090 <http://planeplotter.pbworks.com/w/page/62409382/RTL1090>`_. This can either be done through the config dialog (click on ``OPEN``, toggle the ``Config``-switch and tick the checkmark next to ``/30003 - Basestation type TCP port``), or in the command line: ::

	rtl1090.exe /30003

.. seealso::
	`RTL1090 - Planeplotter Wiki <http://planeplotter.pbworks.com/w/page/62409382/RTL1090>`_