-- Migration: Add password reset fields to users table
-- Run this SQL script on your PostgreSQL database

-- Add reset_token column
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR;

-- Add reset_token_expires column
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP WITH TIME ZONE;

-- Create index on reset_token for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token);

-- Comments
COMMENT ON COLUMN users.reset_token IS 'Secure token for password reset';
COMMENT ON COLUMN users.reset_token_expires IS 'Expiration timestamp for password reset token';

