CREATE INDEX stories_story_publish_date_status
  ON stories_story (publish_date DESC, status);