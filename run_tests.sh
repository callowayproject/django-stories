#!/bin/bash

echo "StoryTests"
./example/manage.py test stories.StoryTests
echo "AuthorTest"
./example/manage.py test stories.AuthorTests --settings=settings_authors
echo "CategoryTests"
./example/manage.py test stories.CategoryTests --settings=settings_categories
echo "PrintTests"
./example/manage.py test stories.PrintTests --settings=settings_print
echo "RelationTests"
./example/manage.py test stories.RelationTests --settings=settings_relations
echo "WidgetTests"
./example/manage.py test stories.WidgetTests --settings=settings_widget