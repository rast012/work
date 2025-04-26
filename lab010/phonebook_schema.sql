-- Drop table if exists
DROP TABLE IF EXISTS contacts;

-- Create contacts table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on names for faster search
CREATE INDEX idx_contacts_names ON contacts(first_name, last_name);

-- Create index on phone number for faster search
CREATE INDEX idx_contacts_phone ON contacts(phone_number);

-- Create procedure to insert a new user or update if exists
CREATE OR REPLACE PROCEDURE insert_or_update_contact(
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_phone_number VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Check if the user already exists
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_first_name AND last_name = p_last_name) THEN
        -- Update the phone number
        UPDATE contacts 
        SET phone_number = p_phone_number
        WHERE first_name = p_first_name AND last_name = p_last_name;
    ELSE
        -- Insert new user
        INSERT INTO contacts (first_name, last_name, phone_number)
        VALUES (p_first_name, p_last_name, p_phone_number);
    END IF;
END;
$$;

-- Create procedure to insert multiple contacts
CREATE OR REPLACE PROCEDURE insert_multiple_contacts(
    p_contacts TEXT[][]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    invalid_records TEXT := '';
    first_name VARCHAR(50);
    last_name VARCHAR(50);
    phone_number VARCHAR(20);
BEGIN
    FOR i IN 1..array_length(p_contacts, 1) LOOP
        first_name := p_contacts[i][1];
        last_name := p_contacts[i][2];
        phone_number := p_contacts[i][3];
        
        -- Simple validation: check if phone number contains only digits, spaces, or special characters
        IF phone_number ~ '^[0-9+\-\(\) ]+$' THEN
            -- Insert or update the contact
            CALL insert_or_update_contact(first_name, last_name, phone_number);
        ELSE
            -- Add to invalid records
            invalid_records := invalid_records || 'Invalid phone: ' || first_name || ' ' || last_name || ' - ' || phone_number || E'\n';
        END IF;
    END LOOP;
    
    -- Return invalid records
    RAISE NOTICE '%', CASE WHEN invalid_records = '' THEN 'All records valid' ELSE invalid_records END;
END;
$$;

-- Create function to query data with pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    created_on TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone_number, c.created_on
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;

-- Create procedure to delete contact by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_identifier VARCHAR(50),
    p_type VARCHAR(10)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_type = 'name' THEN
        DELETE FROM contacts
        WHERE first_name = p_identifier OR last_name = p_identifier;
    ELSIF p_type = 'phone' THEN
        DELETE FROM contacts
        WHERE phone_number = p_identifier;
    ELSE
        RAISE EXCEPTION 'Invalid type. Use "name" or "phone"';
    END IF;
END;
$$;