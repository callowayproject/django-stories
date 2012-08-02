#!/bin/bash

./example/manage.py test stories.StoryTests
./example/manage.py test stories.CategoryTests --settings=settings_categories
./example/manage.py test stories.PrintTests --settings=settings_print
./example/manage.py test stories.RelationTests --settings=settings_relations