# Instructions

## Aim of the project
Our aim here is to demomstrate the use of github copilot (that's you) for product management, business analysis and other aspects of software development which aren't actual coding. We will work on a hypothetical product idea from vision through to writing user stories, but we will not (at least for now) try to write any code or implement anything.

## Project structure
* Project documents should go in the `/docs` folder. 
* Data should go in `/data`.
* Any code written for tactical purposes eg. research or file manipulation should go in `/code`.

## Style guide
All documents should be written in markdown. Filenames should be in dash-case. Use British English.

If you have to write and run any python in the `/code` directory then always remember to use the virtual environment:

```bash
source .venv/bin/activate
```

## User stories

User stories should start with the _As.. I want.. So that_ format. Acceptance criteria should be written using the BDD _Given, Then, When_ format. 

Our engineering will practise TDD, so we should never see separate stories to 'write tests'.

We try to keep our stories small, an individual story should ideally take no more than a couple of days to do.

We should try to make sense of our stories and plan releases by making a story map. Make these in an SVG format.

Stories should be written as github issues with a label 'story'. You can use the gh cli to create these like this:

```bash
gh issue create --label story --label backlog --title "Test story" --body "Body text"
```

I have created labels to represent the workflow of our stories - "backlog" when the story is just a title or placeholder. "ready for dev" when it is fleshed out and ready to go. "in development" when  it is being worked on.

### Tips for writing good user stories

See [writing good user stories](writing-good-user-stories.md).


