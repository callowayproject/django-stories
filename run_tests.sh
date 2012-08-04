#!/bin/bash

echo "StoryTests"
./example/manage.py test stories.StoryTests
echo "CategoryTests"
./example/manage.py test stories.CategoryTests --settings=settings_categories
echo "PrintTests"
./example/manage.py test stories.PrintTests --settings=settings_print
echo "RelationTests"
./example/manage.py test stories.RelationTests --settings=settings_relations