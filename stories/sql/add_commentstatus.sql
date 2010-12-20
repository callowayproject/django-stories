ALTER TABLE stories_story ADD COLUMN "comment_status" integer NOT NULL DEFAULT 1;
UPDATE stories_story SET comment_status = 0 WHERE comments = false;
