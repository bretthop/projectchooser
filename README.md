#Project Chooser

A simple application that provides users with the ability to vote for specific projects to work on.

##More Info

The idea is that a user can log in and create a Project Domain that defines the scope of the Proposals
that other users add. Once this is done, users can vote on Proposals that they are interested in
working on or seeing completed.

At the moment, the application only supports one Project Domain (all Proposals are treated as being part
 of the same domain).

This project is in very early stages of development and only has the basics set up.

##Technologies Used

This application is currently using the following technologies:

* Google App Engine with Python
* Python 2.7
* Twitter Bootstrap

##Current Development Status

* A user can add as many new proposals as they want
* A user has limited (1xGOLD, 1xSILVER, 1xBRONZE) votes as their resource
* A user can see their profile and vote resources
* Voting for a proposal will decrease number of remaining votes
* Withdrawing from a proposal will increase number of remaining votes
* All client request are done via AJAX using JSON (de)serialisation

##REST Interface

This application uses a REST interface for server-client communication. If you
are really interested in which resources are available (and which HTTP methods they provide) then feel free
to look in the 'Resources' package (it's all pretty straight forward).

This section will focus on the general behaviour of the REST interface. In particular; the ability to filter each
response, and the structure of each response.

###Response Structure

* TODO

###Filter Parameter

Each request to the server can contain an option 'filter' parameter. This can be used to limit the amount of data the
server returns back to you (and therefor increase performance). This is optional, and it is important to note that
if you omit this parameter then you will get everything back (if you are querying for a Proposal then you will get back
the Backer that the Proposal belongs to, as well as all the remaining votes, permissions, and role for that Backer (it
will serialise EVERYTHING)).

The syntax is simple to pick up so i'll just write down the definition of it then list out
some examples.

**Syntax:** objectName(field\[,field\])\[~objectName(field\[,field\])\]

* **\*(\*)** - serialises everything (the default behaviour)
* **\*(status)** - serialises all 'status' fields on all objects
* **Proposal(\*)** - serialises all fields on any 'Proposal' object
* **Proposal(username,email)** - serialises the 'username' and 'email' fields on any 'Proposal' object
* **Proposal(\*)~Backer(\*)** - serialises all fields on any 'Proposal' object AND all fields on any 'Backer' object
* **Backer(role)~Role(\*)~Permission(name)** - serialises the 'role' field on the 'Backer' object AND all fields on the
                                               'Role' object AND the 'name' field on the 'Permission' object

##Known issues

* There is no way (through the application) to delete Proposals
* The JSON encoding is not bullet-proof

##Glossary

This section will contain a list of project jargon and their meanings

* Project Domain (or Project) - A domain that Proposals will belong to, and Users can vote on which Proposal gets implements next within that project
* Proposal - An idea, feature, or unit of work that belongs to a Project Domain. Users vote for Proposals and, when the Voting Duration has finished, the Proposal with the most votes will be selected to be next implemented
* User - A user of the system, their role is to add, and vote for, Proposals
* Voting Duration - An amount of time where a User can vote on Proposals for a given Project Domain. Each Project Domain can have its own Voting Duration.
