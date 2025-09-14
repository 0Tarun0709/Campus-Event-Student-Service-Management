# Documentation of the Process
`note: ` This only includes the Brainstroming ideas/ methods happend to be occured while making of the project, this is only included coz, it would give the recap of the vibe and a Drive-Through/walkthrough of multiple options/methods that occured/found to solve this, and this is not a official README file.
## Reqs
what do we need, since its a problem of OPPs, class for each are required which can be:
- Student
- Event
- Management(why? super class to manage conflicts and all sort of operations)

## note
 - clear implementation of conflict needed,
## COnflict Issue
given the Instruction that, an event is flagged as `invalid` if it conflicts/overlaps with a Time of the other event.
as mentioned:
```
- Check for overlapping events in the same venue or at the same time. 
- Flag violations in schedule if any conflicts exist. 
```

So assuming the Overlap with Time no matter the Venue is marked as Conflict, considering one event happens at a time.
` A series of Event scenario instead of the parallel event schedule`

#### Waiting List
student enters the waiting List when the exisiting seats for the Event are filled,
note the logic for droping from the event is not implementing coz the poc is only focused to showcase the working of waiting list.

for to integrate the upgrade form waiting list to General, in the event summary details, which showcases the Enlisted students fro the event. its funny that i couldnt come up with multiple names, which seems like a Investable time, so to skip it, i have hardcoded the name with a variable string which showcases as
```python
name=f"Test Subject {student_id}"
```

#### Analytics
Speaking of the analytics, thanks to the existing libraries, from the class of `CampusEventManagementSystem` which holds the dict of the Classes which are `Events`, `ServiceRequests`, `Students` storing the objects in this list, helped to get the values easily, and converting them into a dataframe made it possible to load into pandas and showcase it visually through plotly.

#### Service Request Handler.

Since the Service object alone can be presented as a Raw object in the UI, but since the service request need to be updated, hence there need to be dropdown to update the request status, but since this is a Admin level feature, considering the POC level, this is made avaialbe as a standard, this can be restricted by adding profiles, things might get complicated for this poc, hence this can be a note to future scope.

## UI
A Dashboard based UI would be good to have, but like what?
since we will be using `Streamlit`, each tab got each task would be appreciated.
- Will LLM be a good choice to solve service requests? or shld they be just a dummp requestss? guess this shld be the last thing to worry, when all the cards are placed.
- Considering the Streamlit made it challenging to showcase the application demo but tracking the session state everytime you add the new one.
- A crazy Integration could be phenomenal, which is ` Integrating the Streamlit-flow into it`
- this would be a graphical representation of the flow of event/conflict of event in a graphical representtion, that would really be agood interation, but tracking the session track everytime is an issue in the streamlit flow, not worth for a POC

