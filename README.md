## This is an assignment for INFO1112 2020 S2

Failure to comply with the Student Plagiarism: Coursework Policy and Procedure can lead to severe penalties as outlined under Chapter 8 of the University of Sydney By-Law 1999 (as amended). These penalties may be imposed in cases where any significant portion of my submitted work has been copied without proper acknowledgement from other sources, including published works, the Internet, existing programs, the work of other students, or work previously submitted for other awards or assessments.


## Introduction

This is a web server that can handle multiple connections and execute applications that are compliant with a subset of the Common Gateway Interface specification. The Common Gateway Interface is used by web-servers to allow compatible programs to be executed on the server, to process HTTP requests and compute a HTTP response. The web-server uses standard input and output as well as environment variables for communication between the CGI program and the itself. HTTP requests that are received by the web-server can be passed to a CGI program via shell environment variables and standard input.

## For Marker
Testcases are under the `mytestcases` floder.

You can run `autotest.sh` to execute all testcases.

### Extension Part:

The program can handle POST request and accepting form data.
If the post request is in cgi script, it will pass the post request content body to the cgi script by Environment Variables and excute the cgi script. If it is not request in a cgi script, it will return a html file shows the form data that the client post.


