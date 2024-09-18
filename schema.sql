-- DROP TABLE if EXISTS user;
DROP TABLE if EXISTS sessionCookies;


-- CREATE TABLE user (
--     userId GUID  PRIMARY KEY,
--     username TEXT UNIQUE NOT NULL,
--     aadhar INTEGER UNIQUE NOT NULL,
--     userpass TEXT NOT NULL,
--     profileUrl TEXT DEFAULT 'DYNAMIC'
-- );

CREATE TABLE sessionCookies (
    cookieId GUID PRIMARY KEY,
    userId GUID NOT NULL,
    expiry TIMESTAMP NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deviceId GUID NOT NULL,
    FOREIGN KEY (userId) REFERENCES user (userId) 
);