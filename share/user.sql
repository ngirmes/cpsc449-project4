PRAGMA foreign_KEYs=ON;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS user;
CREATE TABLE user( 
    username TEXT NOT NULL, 
    passwrd TEXT NOT NULL, 
    UNIQUE(username)
);
COMMIT;
