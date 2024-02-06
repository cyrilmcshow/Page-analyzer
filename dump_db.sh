#!/usr/bin/env bash

pg_dump -a -d $DATABASE_URL > db.dump