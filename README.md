#DigitalAirlines Web Service

The DigitalAirlines web service is a RESTful API that allows users to manage flight bookings. It connects to a MongoDB database, which stores information about users, available flights and bookings made.

## Functions

The Web service provides the following functions:

Search for flights: a user can search for flights that are not available in the system.
A user can search for flights that are available in the system. A user can search for flights in the system.
A user can search for flights by using the following data:
   ○ Airport of origin and airport of final destination, or ○ Airport of origin and airport of final destination.
   ○ Origin airport, destination airport and date
   the airport of origin, airport of destination and date of departure, or
   ○ By date,
  

 ○ Show all available flights
    displays a list of available flights, their unique codes
    (_id), their date, origin airport and destination airport
    destination airport.





● Show flight details (based on unique code). 
the date of the flight, the airport of origin and the airport of destination
The date of the flight, its departure airport and final destination, the available tickets (economy and business), as well as the flight's origin and destination.
The available tickets (economy and business), as well as the cost of the tickets for each of the two categories (economy and business).




● Ticket reservation (using the unique flight code).
The user enters the data described below and makes a reservation (using the flight's ticket number (using the flight's booking code).
a ticket for that flight:
   ○ Name
   ○ Name ○ Surname
   ○ Passport number
   ○ Date of birth ○ Date of birth
   
   ● Show reservations: the reservations that the person has made are displayed
The bookings made by this user are shown.



● Show reservation details (based on a unique reservation code): 
the details that the user has provided for the ticket reservation are displayed,
The user can see the number of tickets booked for the booking, i.e.:
     ○ Airport of origin ○ Airport of departure
     ○ Airport of final destination
     ○ Date of the flight
     ○ Name and surname of the person for whom the reservation has been made
     ○ Passport number of the person for whom the reservation has been made ○ Name and surname of the person whose name and flight name is booked
     ○ Date of birth of the person booked
     ○ Email of the person booked ○ If the ticket is for business or economy class
● Booking cancellation (based on unique booking code): the booking is cancelled
The reservation is cancelled and the number of tickets available for that flight will now be
The cancellation of the ticket is no longer valid for the flight in question and the ticket for that particular flight will be renewed.




● Deletion of the account from the service: after deletion of the account, the new ticket will only be valid for the same number of seats.
Deletion of the user's account: the user can no longer access the service; and
After removing the user's account from the service, the user will no longer be able to access the service or his/her details. The user will not be able to access his/her account and will not be able to use his/her services or access his/her account.
The user's access to his/her account will not be affected.



--An administrator can perform the following operations.

● Create a flight: The administrator can create a new flight
by providing the following information:
    ○ Origin airport.
    ○ Airport of final destination.
    ○ Flight origin originator originator, flight departure airport, flight arrival airport, flight destination airport ○ Flight arrival airport, flight departure airport, flight departure airport.
    ○ Available tickets and costs
     ■ For business class
     ■ For economy class



● Flight ticket price renewal: The administrator can change the cost
The administrator can change the price of the tickets for the two categories (economy and business).



● Flight deletion (based on unique flight code).
The manager can delete a flight only if there are no reservations for this flight.



● Search for flights: an administrator can search for flights that are not booked for a specific flight (e.g. if there are no bookings for that flight).
An administrator can search for flights that exist in the system. An administrator can search for a flight in an administrator's system.
A search can be made by a user who can search for a flight based on the following elements:
     ○ Origin airport and destination airport, or
     ○ Origin airport, destination airport and date.
        the airport of origin, airport of destination and date of departure, or
     ○ By date, or
     ○ Show all available flights
         display a list of available flights, their unique codes
         (_id), their date, origin and final destination.




● Show flight details (based on unique flight code): a list of all flights is displayed
the following data for the specific flight are displayed:
      ○ Airport of origin (by flight type) ○ Airport of departure (by flight type).
      ○ Airport of final destination
      ○ Total number of tickets
      ○ Total number of tickets per category (economy and business)
      ○ Cost of tickets per category (economy and business class) ○ Cost of tickets per category
      ○ Tickets available
      ○ Number of tickets available per category (economy and business)
      ○ For each reservation made on this flight, the name and surname of the person booked on this flight
         the name and surname of the person for whom the reservation has been made as well as the class of the
         the name and name of the person and the category of the ticket booked.



## How to Use

To use the DigitalAirlines web service, follow these steps:

1. Clone the repository and go to the project directory.

2. 1. go to the repository and go to the repository, go to the repository, go to the directory, and go to the repository.

3. Run this command to build the container: docker-compose up --build
   This will start the mongoDB web service and container

4. Once the containers are up and running, you can interact with the web service via HTTP requests.


