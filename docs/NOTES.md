\# Questions



1. Walk through a request end-to-end. You type http://localhost:8000/transactions/ in the browser and press Enter. Describe step by step: what the browser does, what it sends, what the server does, what comes back, what the browser does with the response. Include: why DNS is trivial for localhost, what the TCP connection is for, what an HTTP request line and headers are, and what the response contains.



2\. GET vs POST. What's the difference in purpose (not just "one has a body")? Give one concrete example of each from Ledgr — one that would be a GET and one that would be a POST. Hint: creating a transaction is one of them.



3\. Status codes. What does a 302 mean, and why would a web app ever respond with a redirect instead of the content the user wanted? Give a specific Ledgr example where a 302 is the correct response. (You'll implement this in Phase 3 — POST-redirect-GET — so struggle with it now.)



4\. Cookies and sessions in one breath. What is a cookie? What is a session? What is the relationship? (One sentence each, then one sentence linking all three.) Then: when you log into a Django app, what exactly is stored in the cookie — the user's ID, their password, or something else?



5\. http://localhost:8000 vs https://ledgr.example.com. Two differences: one about transport security, one about who the server is. Explain both. Then: why does localhost use http and not https?



6\. Client-side vs server-side databases. Why can't Django read from IndexedDB (the browser's database)? What is the difference between "SQLite on the user's machine" and "SQLite inside the browser"? (This is the question we spent the most time on earlier — write it down as if explaining to a friend who's making the same mistake you did.)



\# Answers



1\. The browser looks for the DNS server pointing to that url and serves the webpage from that url. Since it is hosted on your computer a DNS server is not required. 8000 is the port that it is running on. different traffic can run on the same IP address of a server as long as there are free ports, port 8000 is running the web server in this instance. An HTTP request line is sent by the browser or the user-agent to retreive a specific web page or website. headers contain additional information , here a request header may be used to add more information like which computer is sending the request. the response can load HTML content and images and a script can be used to request any other relevant information from the relevant servers like ads from an ad server and videos from a video server



2\. GET is when the user wants data from the server and POST is used to add data sent by the user onto the server. A GET request in Ledgr may be used to view the transactions from the database whereas adding a transaction will send a post request to the server to add that transaction into the database



3\. a 302 code happens when the client sends a get request and the data is available but the user is redirected regardless. in my app this may be if the user is not logged in but he wants to view the transactions the data will be available but the browser will redirect him to the login page before he can view transactiosn



4\. a cookie is used to add state information because HTTP by default is stateless. while cookies may not contain login information (maybe they could but its not secure) they can use a cookie to check if the user has previously logged in and if yes they get to bypass the login which saves the user some time. these cookies can also have an expiration date so the user will not stay logged in forever. a session is a temporary memory that allows the browser or server to remember who the user is throughout multiple page clicks. for example the user logs into ledgr and sees the view transactions the server knows to show the user HIS data, when he clicks onto the analytics page the browser has to remember its still the same user's data the analytics must reflect



5\. http is unsecure whereas https is secure, it uses the TLS protocol and a 3 way handhshake to validate the ssl certificate of the server. localhost means that the server is in your own computer whereas https://ledgr.example.com is redirecting to an example.com subdomain within the ledgr domain this may be an external server which is why it is important that data is sent and received securely between the user and the server



6\. client side is when the information is stored on the browser. it can only be accessed on that particular browser. server side is where the information is localised within a server , the user can use any browser and still access their transactions as long as they are able to connect to their computer (server) where their transactions are stored





\# Corrected Rewritten Answers



1. The browser has an exception when hostname is localhost so it directly points to 127.0.0.1 or the IPv6 equivalent. A TCP connection is established between the client and the server to make sure that the session is connection-oriented as this is much more reliable than a connectionless protocol like UDP. The browser sends a request to the server and it gets back relevant information, this can be images or HTML or anything else. Loading a single webpage takes multiple HTTP requests from the browser and responses from the server.
2. GET is used to request data from the server by the client whereas POST is used by the client to send data onto the server. GET is idempotent (what this means is that doing GET for the same data 5 times will give you back the same data) whereas creating a POST request for a transaction 5 times will create 5 new transactions on the server
3. the 302 status code is when the user sends a GET request to the server but the server redirects the user to another url. In Ledgr this may happen when the user sends a GET request to view financial data but when the server checks for authentication the user is not logged in so it refuses to send the transaction data and instead redirects the user to the login page. It is important to know that the 302 status code only has a location pointer to redirect and does not have any content inside it.
4. cookies are used to store data. in Django cookies have a session id that points to a session database where any relevant information will be stored. An example of a cookie being used may be when the user has previously logged in and the cookie has not expired yet, when the go to the login page Django will look up the session id in the cookie and check the database if the cookie has expired and if the user has logged in previously they are redirected to the transactions page. once the cookie expires they will have to login again. A session is server-side and a cookie points to the session which can be used to store state information since by default HTTP is stateless, the use of cookies and sessions enables this functionality
5. ledgr is a subdomain of example.com. localhost:8000 means that the web server is running on the user's computer on port 8000 whereas https://ledgr.example.com is the url that points to another remote server. the DNS server finds the IP address of the domain name and a secure connection between the client and server is established and the data sent between the client and server is encrypted thanks to HTTPS. It uses TLS protocol which has a TLS handshake that validates the SSL certificate. Localhost uses HTTP because the connection never leaves the home server
6. Client side database will live in the browser as a JS  API, server side databases live on a computer. A user using ledgr from a different browser will not be able to access their transaction data because it is not stored on that browser and moreover Django uses python so it will not be able to communicate with the database natively. Ledgr can access the database within the machine as the data is stored locally but if someone wants to access their transaction data from another machine they will not be able to do so because the database is localized to their machine.

