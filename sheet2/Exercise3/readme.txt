Improper auth validation

There is a hidden field using the user id. It is possible to change
it to the id of support (admin). With this it's possible to see the list of transactions of all users.

The patch makes the field get the id of the user whose
session is active.
