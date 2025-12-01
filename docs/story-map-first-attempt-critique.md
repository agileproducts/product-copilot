# Critique of the first attempt at a story nap

This is a decent attempt at a story map. But there are some things I think we should change.

1. Configuring GCP or deploying a cloud function are tasks, not stories. These are things we would do as part of stories to deliver real working software. So I don't think they belong on a story map.
2. I like story maps in which you would move along the top row to deliver a steel thread. But in this map you would have to work down some of the columns first.
3. You have a column about tracking/storing data which comes after sending an alert, this is the wrong way around isn't it?
4. You have a story to 'structure logging'. This is a task. What story would you do involving logging that did not involve structring it.
5.  End-to-end test is not a story. Remember we are doing TDD and CI/CD. Our software is *always* tested end to end as part of our deployment pipeline.
6. Now I think of it, setting up a deployment pipeline is the kind of thing that can absorb a lot of time in a story that I'd prefer to have visibility of. Maybe we should identify this as a kind of iteration 0 prerequisite. 
7. You don't need to add time estimates to these stories. You aren't the coder, yet. 