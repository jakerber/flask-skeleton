/**
 * SQL Development script
 *
 * https://www.tutorialspoint.com/postgresql/index.htm
 *
 *  - Inserts test data into a development database.
 *  - Tables are created automatically during app initialization.
 */

-- Sample user table entries
INSERT INTO users (id, phone, name, password, created_on)
VALUES
    (1, 1111111111, 'josh', '1a0a41d838bbff454688436ff593508dab2c55722bae0f32d6ba50975a6a46a3', 'Wed, 12 May 2021 02:20:01 GMT'),
    (2, 2222222222, 'joey', 'dc6a8cfa75129796c929f93a4dbe914604f71ea27f7d0ff6d8ed72d75226ecd7', 'Wed, 12 May 2021 02:20:02 GMT'),
    (3, 3333333333, 'alec', 'efd851b3a9fc641a5316e0c8cff544c070448ffadf9772348b5391dd02ad2f89', 'Wed, 12 May 2021 02:20:03 GMT');

-- Sample stuff table entries
INSERT INTO stuff (description, user_id, created_on)
VALUES
    ('stuff-josh-owns', 1, 'Wed, 12 May 2021 02:20:04 GMT'),
    ('stuff-joey-owns', 2, 'Wed, 12 May 2021 02:20:05 GMT'),
    ('stuff-alec-owns', 3, 'Wed, 12 May 2021 02:20:06 GMT');

-- Sample auth_token_blacklist table entries
INSERT INTO auth_token_blacklist (token, created_on)
VALUES
    ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjA4MDA2NzEsImlhdCI6MTYyMDgwMDQ5MSwic3ViIjoyLCJpcGEiOiIxMjcuMC4wLjEifQ.OijYY0CvOb3w-Noh_ZLNcWWC3iET8CzCH8E1RiWb3FI', 'Wed, 12 May 2021 02:20:07 GMT');
