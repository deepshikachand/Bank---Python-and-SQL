CREATE TABLE accountmaster (
    Account_Number INTEGER PRIMARY KEY,
    name CHAR(40),
    Account_Type CHAR(40),
    DateOfOpening DATE,
    Address_1 CHAR(100),
    Address_2 CHAR(100),
    City CHAR(20),
    Opening_Balance INTEGER
);

CREATE TABLE Transaction (
    Account_Number INTEGER,
    Date DATE,
    Transaction_Type CHAR(1),
    Amount INTEGER
);
