/**
 * SQL Development script
 *
 * https://www.tutorialspoint.com/postgresql/index.htm
 *
 *  - Inserts test data into a development database.
 *  - Tables are created automatically during app initialization.
 */

-- Example user table
INSERT INTO users (phone, name, password)
VALUES
    (9784605401, 'josh', '1a0a41d838bbff454688436ff593508dab2c55722bae0f32d6ba50975a6a46a3'),
    (9784605212, 'joey', 'dc6a8cfa75129796c929f93a4dbe914604f71ea27f7d0ff6d8ed72d75226ecd7'),
    (9784605240, 'alec', 'efd851b3a9fc641a5316e0c8cff544c070448ffadf9772348b5391dd02ad2f89');

-- Example item table
INSERT INTO items (value, owner)
VALUES
    ('item-josh-owns', 9784605401),
    ('item-joey-owns', 9784605212),
    ('item-alec-owns', 9784605240);
