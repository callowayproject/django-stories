#!/bin/bash

echo "StoryTests"
./example/manage.py test stories.tests.StoryTests
echo "AuthorTest"
./example/manage.py test stories.tests.AuthorTests --settings=settings_authors
echo "CategoryTests"
./example/manage.py test stories.tests.CategoryTests --settings=settings_categories
echo "PrintTests"
./example/manage.py test stories.tests.PrintTests --settings=settings_print
echo "RelationTests"
./example/manage.py test stories.tests.RelationTests --settings=settings_relations
echo "WidgetTests"
./example/manage.py test stories.tests.WidgetTests --settings=settings_widget