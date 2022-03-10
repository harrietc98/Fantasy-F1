# Fantasy-F1

To do:
- At present, it picks a driver one at a time from best to worst- instead, want to consider all combinations and pick one that maximises points and best utilises budget
- Incorporate constructor into team
- Add features so it's not purely based on points/million
- Add targets of best teams for each race week in 2021 season to df, see if can predict using combination of features
- Add injured driver function
- Account for changing drivers between seasons

Feature ideas:
- General 
  - Seasons competed in
  - Final placing in 2021 season
- Week specific
  - Placing at track in 2021 season
  - Performance in Q1, Q2, Q3 if possible


### General thoughts

Look at best fantasy f1 team each race week last season and see if model predicts that team given the above features (can either do a test-train split over 2021 season- preferable for driver consistency, or use 2021 as the test and previous years as the training etc)

Targets are the best teams each race week- make binary classifier of 0 (not in team) or 1 (in team) to see if we can minimise error to predicting targets with a combination of the above features


Constraints:
- No drivers=5
- No constructors=1
- Max budget=100
- Want to maximise points per million