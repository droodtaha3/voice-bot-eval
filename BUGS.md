Bugs I found in the clinic's AI agent:

These come from my 10 calls in the `calls` folder. I listened to the recordings to check each one, because my own speech-to-text can mishear words. The timestamps come from the transcript files, so they can be a few seconds off from the audio.

1. It gives two different cities for the same clinic

In call 04 (hours, around 0:45), I asked where the clinic is, and the agent said 1234 Recovery Way, Suite 200, in Austin. In call 01 (reschedule, around 0:54), the same agent told me my appointment was with Kelly Noble at a Nashville location, 220 Athens Way. That is two different cities for one clinic. A patient could drive to the wrong city for their visit. I think this is the most serious problem I found. The agent should give one location every time, or ask which location the patient means.

2. It talks about weekend openings, but the clinic has no weekend hours

In call 04 (around 0:16 to 0:31), the agent said the clinic is open Monday, Tuesday, and Thursday from 9 to 4, Wednesday from 12 to 7, and Friday from 9 to 12. It never mentioned the weekend. Then in call 05 (around 1:38 to 2:19), I asked for a Sunday appointment at 10 AM, and then for any weekend appointment. The agent said there were no weekend openings, but it never said the clinic is closed on weekends. It even offered to check again for weekend openings later. That sounds like weekend slots might show up one day, which doesn't match its own hours. It did the right thing by not booking me for Sunday, but it should have said the office is closed on weekends and offered the next weekday.

3. It calls the caller "Drew," and I signed up as Drood

At the start of call 01 (around 0:26), before asking me anything, the agent said it saw I was calling from the number on file and asked, "Am I speaking with Drew?" I signed up for the demo as Drood Taha, so that name doesn't match. My bot answered that it was Drood. The agent didn't say anything about the mismatch. It just asked for my date of birth and then read out my appointment details. The same opener shows up in 8 of my 10 transcripts. In most of those calls my bot simply said "yes," so call 01 is the only one where the name was corrected, and that is the call that backs this up. The problem is that the agent says a name before it knows who is calling, and then shares appointment details after only a first name and a date of birth. It should ask the caller for their full name and stop if it doesn't match the record.

4. It sends a refill request without checking what is being refilled

In call 03 (around 0:50 and 1:13), I asked for a refill of meloxicam 15 mg. The agent said it didn't see any medications on the chart that it could refill. When I asked it to send the request anyway, it said it had sent it to the clinic support team and that they would get back to me within one business day. It never repeated the medication, never asked which pharmacy to use, and never said the request couldn't be matched to a prescription. The patient leaves thinking the refill is handled, and the clinic gets a request that is hard to act on. It should confirm the medication and pharmacy, and say clearly that it couldn't find the prescription.

What it did well:

I only checked these in the transcripts, not in the audio. In call 05, it did not book a Sunday appointment. In call 09 (the post-surgery pain call), it said it couldn't give medical advice and told the caller to call 911 or go to the emergency room, twice. In call 06, it did not make up a copay or coverage amount and told the caller to ask their insurance company. In call 08, it handled a change of day and time correctly.