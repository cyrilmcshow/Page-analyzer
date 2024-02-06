#!/usr/bin/env bash

psql -a -d postgresql://postgres:366552@localhost:5432/page_analyzer_db -f database.sql
psql -d postgresql://postgres:366552@localhost:5432/page_analyzer_db < db.dump