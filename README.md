Project Chooser
==============

A simple application that provides users with the ability to vote for specific projects to work on.

More Info
--------------

The idea is that a user can log in and create a Project Domain that defines the scope of the Proposals
that other users add. Once this is done, users can vote on Proposals that they are interested in
working on or seeing completed.

At the moment, the application only supports one Project Domain (all Proposals are treated as being part
 of the same domain).

This project is in very early stages of development and only has the basics set up.

Technologies Used
--------------

This application is currently using the following technologies:

* Google App Engine with Python
* Python 2.7
* Twitter Bootstrap

Current Development Status
--------------

* A user can add as many new proposals as they want
* A user has limited (1xGOLD, 1xSILVER, 1xBRONZE) votes as their resource
* A user can see their profile and vote resources
* Voting for a proposal will decrease number of remaining votes
* Withdrawing from a proposal will increase number of remaining votes
* Anyone with a Google Account can log in and add/vote for project proposals
* All client request are done via AJAX using JSON (de)serialisation

Known issues
--------------

* There is no way (through the application) to delete Proposals
* The JSON encoding is not bullet-proof
* Current JSON library seems to be doing solid job but strongly depends on custom static jsonFields() method

Glossary
--------------

This section will contain a list of project jargon and their meanings

* Project Domain (or Project) - A domain that Proposals will belong to, and Users can vote on which Proposal gets implements next within that project
* Proposal - An idea, feature, or unit of work that belongs to a Project Domain. Users vote for Proposals and, when the Voting Duration has finished, the Proposal with the most votes will be selected to be next implemented
* User - A user of the system, their role is to add, and vote for, Proposals
* Voting Duration - An amount of time where a User can vote on Proposals for a given Project Domain. Each Project Domain can have its own Voting Duration.
