


# Project Scope

This document outlines what is in and out of scope for the project. It will
change and evolve as the program does.

**Project version:** v1.0.0 – Hondana

## In Scope

- A simple command line tool (CLT) that works with a MySQL database to
  organize a user's manga collection
- Search for series by full or partial title
- Select between editions of a series, with ownership tracked per edition
- View owned and missing volumes and collection completion percentage
- Add or remove volumes from a user's collection (single volumes, multiple
  volumes, and ranges such as `1,3-5,8`)
- Import series, edition, and volume data via a Python script and a `.json`
  catalog file
- A quick setup guide in the GitHub README

## Out of Scope (v1.0.0)

- Adding new series via the command line (series come from the `.json`
  catalog in v1)
- Editing series or edition details after import

## Deferred

Not part of v1.0.0, but planned or under consideration for future versions:

- **CLT improvements:** add new series, editions, and volumes from the
  command line; edit series and edition details; export the collection
  to `.json` or `.csv`
- **Code quality:** automated tests and a changelog
- **Backend API:** expose collection features through an API
- **Web interface:** a simple front end for searching and managing a
  collection
- **Longer term:** user accounts, wishlist tracking, cover images
