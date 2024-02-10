#!/usr/bin/env bash

pg_dump -a -d postgresql://postgres:366552@localhost:5432/page_analyzer_db > db.dump