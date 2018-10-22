Joe Warner
10/22/2018
Response to Campaign Monitor Coding Challenge

Summary - 
I built a simple Django app for the coding challenge
Assumptions / pre-requisites:
  Virtual Environment Installed
  	$>  mkvirtualenv challenge
       (challenge) $>           #Denotes challenge env is active

  Install Dependancies
        (challenge) $> pip install -r requirements.txt
  
  Test it out
	(challenge) $> cd <your target dir>
        (challenge) $> python manage.py test

  Some brief Explanation:
	I chose Django b/c that's what I'm working with, and am at work, and didn't have a lot of time.
	For the record, I use Django a lot, but rarely (if ever) use the built in ORM - instead I use SQLAlchemy.
	
	Approach:
		Assumptions:  I put the list of URI/URL's to test in an array in the tests.py file.
		I setup a test to iterate over each item in the array.
		For each item (a uri):
			I use the python requests library to perform a "get"
			I manage two exceptions right now - 
				InvalidSchema - (eg. jttps://www.cnn.com)
				ConnectionError - (eg. http://fogettaboutit.com)
			You could easily add other exceptions as needed

	If I had extra time:
		Could the function be improved if the same list of links is being passed in many times ?
		
		Joe: Sure, I would start by adding date/time to my link status wrapper object, 
		persisting the wrapper objects (in some database - I like redis).  
		For each URI - I would query my database/store - and check the last time checked.
		If the time delta between now and last time checked is greater than some time delta, 
		Run the test, and store the new results.
		
		How might the function be written to process arbitrarily long lists of lengths ?
		
		Joe: Really long lists can (possibly) take up a LOT of memory.  
               Look into python generators to efficently handle iterating over a list 
               in a lazy fashion - uses MUCH less memory.
		
		How might this function exposed as an HTTP API to be used by a front-end app ?

		I would add an endpoint in challenge/urls.py that will be exposed by Django.
		I would also add a View in link_checker/views.py that will process the view 
		and return JSON.
		Next, assuming I'm deploying this on a linux box (or virtual box) - I would 
		setup the app to run as a uwsgi app - using Supervisor to control it and have the logs
		sent to syslog.  I would setup nginx as the forward facing endpoint  web server - 
		having it reverse proxy requests to the uwsgi app.  A bit simpler than Apache


Initial Challenge:
 See Link Validator Original Request
