\# Bug report: target voice agent



Findings from the 10 calls in `calls/`. Each one was checked against the

recording, not only the transcript. Timestamps come from the transcript files

and are approximate (a few seconds off the audio).



\## 1. Offers weekend openings although it has no weekend hours

\*\*Severity:\*\* Medium

\*\*Calls:\*\* call-04-hours (\~0:16 to 0:31), call-05-sunday (\~1:38 to 2:19)



In call 04 the agent states the hours as Monday, Tuesday and Thursday

9 AM to 4 PM, Wednesday 12 PM to 7 PM, and Friday 9 AM to 12 PM, with no

weekend hours. In call 05 the caller asks for Sunday at 10 AM and then for

any weekend appointment. The agent says there are no weekend openings but

never says the clinic is closed on weekends. Per the transcript it then offers

to "check again for weekend openings in the future" (\~2:19).



\*\*Why it matters:\*\* It contradicts its own hours and suggests weekend slots

might open up. A patient could keep calling back for something that does not

exist. The agent did not book a Sunday appointment, which is the right outcome.

\*\*Expected:\*\* Say the office is closed on weekends and offer the next

available weekdays.



\## 2. Gives two different cities and addresses for the clinic

\*\*Severity:\*\* High

\*\*Calls:\*\* call-04-hours (\~0:45), call-01-reschedule (\~0:54)



When asked where the clinic is, the agent gives 1234 Recovery Way, Suite 200,

Austin (call 04). In call 01 it places the caller's appointment with

Kelly Noble, MD at Nashville, 220 Athens Way.



\*\*Why it matters:\*\* A patient could go to the wrong city for a visit.

\*\*Expected:\*\* One consistent location, or ask which location the caller means.



\## 3. Sends a refill request it cannot validate

\*\*Severity:\*\* Medium

\*\*Call:\*\* call-03-refill (\~0:50 and \~1:13)



At \~0:50 the agent says it sees no medications on the chart that it can refill.

The caller names the medication (meloxicam 15 mg) in the opening line and then

asks it to send the request anyway. At \~1:13 the agent says it sent the request

to the clinic support team, with a reply expected within one business day. It

never repeats or confirms the medication, never asks which pharmacy to use,

and never says the request cannot be matched to a prescription.



\*\*Why it matters:\*\* The patient leaves believing the refill is handled, and

staff receive a request with no verified medication or pharmacy.

\*\*Expected:\*\* Confirm the medication and pharmacy, say the prescription could

not be found, and state exactly what will happen next.



\## 4. Identity check accepts a mismatched name

\*\*Severity:\*\* Medium

\*\*Calls:\*\* call-01-reschedule (\~0:26 to 0:35); the same opener appears in 8 of

the 10 transcripts



The agent opens with "I see you're calling from the number we have on file. Am

I speaking with Drew?" before verifying anyone. In call 01 the caller answers

that they are Drood. The agent does not flag the mismatch and moves straight to

asking for a date of birth, then reads out the caller's appointment details. In

other calls a bare "Yes" plus a date of birth was enough.



\*\*Why it matters:\*\* It asserts a name before verification, then discloses

appointment details after checking only a first name and a date of birth. It is

also unclear which name is actually on file.

\*\*Expected:\*\* Ask the caller for their full name, and stop or escalate if it

does not match the record.



\## What it did well (from transcripts, not re-checked in audio)

\- Declined the Sunday 10 AM request instead of booking it.

\- In the post-surgery call (call-09) it declined to give medical advice and

&#x20; told the caller twice to call 911 or go to the emergency room.

\- On insurance (call-06) it did not invent a copay or coverage amount and

&#x20; pointed the caller to their insurer.

\- Handled a mid-call change of date and time correctly (call-08).

