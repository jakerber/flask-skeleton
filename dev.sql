/**
 * SQL Development script
 *
 * https://www.tutorialspoint.com/postgresql/index.htm
 *
 *  - Inserts test data into a development database.
 *  - Tables are created automatically during app initialization.
 */

-- Example user table
INSERT INTO users (phone, name, password, created_on)
VALUES
    (9784605401, 'josh', '1a0a41d838bbff454688436ff593508dab2c55722bae0f32d6ba50975a6a46a3', 'Wed, 12 May 2021 02:20:01 GMT'),
    (9784605212, 'joey', 'dc6a8cfa75129796c929f93a4dbe914604f71ea27f7d0ff6d8ed72d75226ecd7', 'Wed, 12 May 2021 02:20:02 GMT'),
    (9784605240, 'alec', 'efd851b3a9fc641a5316e0c8cff544c070448ffadf9772348b5391dd02ad2f89', 'Wed, 12 May 2021 02:20:03 GMT');

-- Example item table
INSERT INTO items (value, owner, created_on)
VALUES
    ('item-josh-owns', 9784605401, 'Wed, 12 May 2021 02:20:04 GMT'),
    ('item-joey-owns', 9784605212, 'Wed, 12 May 2021 02:20:05 GMT'),
    ('item-alec-owns', 9784605240, 'Wed, 12 May 2021 02:20:06 GMT');
