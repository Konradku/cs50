-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * 
FROM crime_scene_reports 
WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";
--Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
--Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.
SELECT name, transcript 
FROM interviews 
WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%courthouse%";
--Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. 
--If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
--Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, 
--I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
--Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. 
--In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. 
--The thief then asked the person on the other end of the phone to purchase the flight ticket.
CREATE TABLE suspects AS
SELECT distinct(courthouse_security_logs.license_plate)
FROM courthouse_security_logs
JOIN people ON courthouse_security_logs.license_plate = people.license_plate
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE courthouse_security_logs.year = 2020 AND courthouse_security_logs.month = 7 AND courthouse_security_logs.day = 28
AND courthouse_security_logs.hour = 10 AND courthouse_security_logs.minute <= 25 AND courthouse_security_logs.activity = "exit" AND courthouse_security_logs.license_plate IN
(SELECT license_plate FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE
year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw")));
--suspects' license plates

CREATE TABLE narrow_suspects AS
SELECT * FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60 AND license_plate IN
(SELECT license_plate FROM suspects);
--narrow suspects

SELECT * FROM people WHERE passport_number IN
(SELECT passport_number FROM passengers
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.origin_airport_id IN
(SELECT id FROM airports WHERE city = "Fiftyville")
AND passport_number IN
(SELECT passport_number FROM narrow_suspects)
AND year = 2020 AND month = 7 AND day = 29
ORDER BY hour LIMIT 1);
-- first flight from Fiftyville day 29 month 7, from the suspects - the thief is Ernest

SELECT * FROM people WHERE phone_number IN
(SELECT receiver FROM narrow_suspects WHERE name = 'Ernest');
-- accomplice

SELECT city FROM airports 
WHERE id IN
(SELECT destination_airport_id FROM flights WHERE id IN
(SELECT flight_id FROM passengers WHERE passport_number IN
(SELECT passport_number FROM narrow_suspects WHERE name = "Ernest")));
--destination city London