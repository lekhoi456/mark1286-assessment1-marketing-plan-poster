# Lecture 6 recording — machine transcript

**Machine transcript: verify before quoting.** Speech was transcribed automatically; it is not a verbatim record checked by a human listener. Before any passage is treated as exact evidence, listen to the recording at the stated timestamp.

- Source: `Lecture + Tutorial 6/Lecture 6 - Poster Structure Recap.mp4` (relative to the module root)
- Duration (ffprobe `format=duration`): 1403.008 s (23:23)
- Streams: H.264 video 1920×1080; AAC audio. Audio extracted with ffmpeg to 16 kHz mono WAV in `/tmp` (deleted after use).
- Transcribed: 27 September 2026, locally on Apple silicon; model caches in `~/.cache/huggingface` (outside iCloud).
- Primary text (below): mlx-whisper 0.4.3, model `mlx-community/whisper-large-v3-turbo`; language `en`, word timestamps, `condition_on_previous_text=False`.
- Cross-check: faster-whisper 1.2.1 (CTranslate2 4.8.2), model `medium.en` (Systran), int8 on CPU, beam 5, word timestamps, `condition_on_previous_text=False`.
- Tie-break reading (reported in the register at the end, not used to choose text): mlx-whisper 0.4.3, model `mlx-community/whisper-large-v3-mlx`, same settings as the primary.
- Whole-transcript word agreement (difflib ratio on normalised words): primary vs cross-check 0.975 (3,403 vs 3,377 words); primary vs tie-break 0.975; cross-check vs tie-break 0.969.
- Timestamps `[mm:ss]` are segment starts from the primary model, truncated to whole seconds.
- Markers: `[uncertain: A / B]` = primary (large-v3-turbo) reads A, cross-check (medium.en) reads B, and the difference changes a content word. Not marked: differences only in numerals versus number words, "percent" versus "%", fillers ("uh", "um"), punctuation, capitals, contractions, or insertion/deletion of short function words. Passages where all models agree may still be wrong (see the notes after the transcript).
- Speaker: one voice throughout. The video's title slide (visible 00:00–00:52) reads "Developed & Presented by: Dr. M Arsalan Nazir (Module Leader)"; the extracted `w06-lecture` slide 1 does not carry this line. Speaker identity is inferred from that on-screen text only.
- This file is not a slide source: it has no `## Slide`/`## Page` sections and is not a target for `check_register_quotes.py`.

## Slides visible in the recording (scene-change detection, ffmpeg `scene>0.08`; frames inspected by the agent)

| From | Screen content | Matches current deck `w06-lecture` |
|---|---|---|
| 00:00 | Title: "Week 6 – Lecture", "Midterm Poster (Group Presentations) Structure Recap", presenter line | s1 (presenter line not in the current deck) |
| 00:52 | Learning Objectives | s2 |
| 01:06 | What to Include – Poster Presentation (with a Moodle screenshot showing "Assessment 1 Brief.pdf" and "Mini Case Study - TESLA (Print).pdf") | s3 |
| 02:06 | Black screen; presenter's webcam only | — |
| 05:00 | The poster must include at least the following (precise) information | s4 |
| 05:56 | Hand Drawn Poster Contents (elements 1–4) | s5 |
| 08:52 | Contents (cont.…) (elements 5–8) | s6 |
| 12:45 | Contents (cont.…) (elements 9–11) | s7 |
| 17:30 | Presentation Quality & Grading Elements | s8 |
| 19:38 | "Assessment Schedule" slide: presentation dates in June 2025 and a schedule table | **not in the current deck** |
| 22:34 | "Thank you, and attend your tutorials this week for the group poster presentations / Any Questions? / Email: m.nazir@greenwich.ac.uk" | s9 (email line not in the current deck's extracted text) |

The recording therefore shows an earlier version of the deck, delivered to a cohort whose presentations were in June 2025. See `../lecture6-guidance.md`.

## Transcript (primary model, with cross-check markers)

[00:01] Hello students, welcome back. We are in week six and this week topic is the group presentation,
[00:09] the poster, midterm examination. And today I'm just going to give you the brief structure recap
[00:16] because we have discussed important things in week five and I've given you the assignment brief
[00:24] as well in the class. Today we're just going to give you a brief recap again
[00:32] about the structure, what you need to add in your poster presentation because
[00:36] your presentation is going to start this week on Wednesday so before your
[00:43] formal presentation I'm just going to give you the brief information about the
[00:48] assignment brief and what you need to add in your posters.
[00:53] So the learning outcome, developing a comprehensive marketing and sales strategy plan for a company product or services in the future economy.
[01:02] And the assignment brief instructions.
[01:07] OK, so the important thing is what you need to include in your [uncertain: poster / processor] presentation.
[01:14] I have given you the assignment brief in the class and you can download the assignment
[01:19] brief from Moodle as well.
[01:21] But the important thing is what you need to add in your posters.
[01:26] So these are some of the instructions.
[01:28] So the assessment one, the marketing plan and the group poster presentation brief.
[01:33] You need to download the assignment brief.
[01:37] If you have downloaded it, that's fine.
[01:40] we have given you the printouts in the last week session as well so if you have your printouts
[01:47] you can use the printouts as well if you don't have the printouts you can download the assignment
[01:51] brief again from the Moodle and you can see in lecture five we have assignment one brief so this
[02:01] is the actual assignment one brief so you can download this one and just look at the content
[02:07] And then based on this assignment brief instruction, you can draw your poster.
[02:12] So the presentation will be [uncertain: (nothing) / page] delivered in front of the class.
[02:16] Yes, you need to present your poster in the class lasting 15 minutes, followed by five minutes for questions.
[02:23] So maximum 20 minutes with Q&A session.
[02:31] sorry in order to add the contents we have discussed this Tesla case study in lecture
[02:41] four so this case study is all about the sales fundamental and the modern selling techniques
[02:46] so in short this case study will help you to add some contents from the assignment brief and from
[02:56] the case study and you can work on your poster accordingly so you can find this
[03:01] case study in week 4 as you can see in week 4 and the mini case study at Tesla
[03:07] and you can print out this case study I've given you case study in the
[03:12] classrooms as well in your tutorials so if you don't have this case study you
[03:20] can download it from a Moodle as well then the next instruction is all group
[03:27] members must participate in the presentation and submit the poster
[03:30] hand-drawn chart the group poster must be submitted from the individual account
[03:37] and you just need to take a clear picture of the poster from your cell
[03:41] phone and upload it on Moodle for and grading and when submitting on turnitin
[03:47] for the grading include your tutorial room date time and your tutor's name in
[03:53] the subject line make sure to include the names and student numbers the
[04:00] complete student names and the complete student numbers as per the university
[04:04] system of all group members on the poster and clearly indicate which part
[04:10] each member contributed if applicable let's suppose one of the group member
[04:16] he or she contributed and he or she presented the first three slides okay
[04:24] just try to add the name of the [uncertain: and group / Nkruv] member well it's not a mandatory
[04:29] but if you can add it's going to be easy for us it's going to be easy for you as
[04:34] well to explain the slides accordingly so the important thing is guys try to
[04:41] download these files assignment assessment one brief from week five and
[04:47] mini case study Tesla from week four resources and you can take some help
[04:54] from these resources and you can work on your poster accordingly okay and the
[05:02] poster must include at least and the following precise information what
[05:08] company you need to pick what type of the business you can select so for this
[05:15] assessment during a one to two week marketing business bootcamp students
[05:20] will work in groups to develop a comprehensive marketing strategy plan for
[05:24] a real market okay it could be any existing business okay or hypothetical
[05:31] business or you can assume a new business as well okay and based on the
[05:36] current business if the business is already established in the market you can pick any brand
[05:44] any existing brand from the market or you can assume your own business as well and you need
[05:50] to create a marketing plan for the for the selected business okay so hand-drawn poster contents include
[06:01] So the first one you need to add your student and business details for example
[06:07] students should complete their information as per the university registration system including the
[06:12] name of the company and business associated with their assignment. So in simple words you need to
[06:17] add your names, your enrollment information, registration number etc and the name of the
[06:26] business you can add logo as well if you want then and the company and the
[06:32] business introduction what is the background of the company for example
[06:35] could be from any industry yeah you can choose any business from any industry
[06:39] and from any country okay there is no restriction so what are the locations or
[06:45] context of its operation for example could be from any country what product
[06:51] and services does it offer so do one thing just try to add the information in
[06:55] bullet points okay because you have only one poster and we don't want to see too
[07:01] much theoretical information so you can add information in bullet points and
[07:06] when you're presenting your poster try to explain all of the bullet points okay
[07:11] and this is how you can add the information in your poster then what
[07:17] product and services does it offer the next one is target market analysis have
[07:23] you clearly identified and described your target market who are your customers
[07:27] where exactly they're living what are the different segmentation strategies
[07:34] when we say the segmentation have you provided demographic information and
[07:39] their location their age their income psychographic and behavioral
[07:43] characteristics of your target audience based on the hobbies based on their
[07:48] lifestyle based on the personality they are going to buy your product and how
[07:53] did you segment and prioritize your target [uncertain: market / (nothing)] so based on which
[07:57] segmentation you have prioritize your target market and your segments then we
[08:03] have positioning have you define a clear positioning statement for the brand
[08:08] product and service how does your positioning differentiate your brand
[08:12] product service from competitors have you considered the unique value
[08:16] proposition that resonates with your target audience you can take all of the information
[08:20] from lecture four okay again the tesla case study you can find some examples how you can work on the
[08:28] positioning strategy how you can work on the target market analysis because we have covered
[08:33] the examples in week four okay so if you can just look at the week four resources download the week
[08:39] four lecture and seminar resources download the case study and you will find some information how
[08:45] you can connect all of the examples with your company and with your poster contents.
[08:53] Then we have branding and identity. How have you developed the brand identity including logo,
[08:59] color scheme and brand messaging? Does your branding strategy align with the desired
[09:03] positioning and target market? So this is all about the branding and identity.
[09:07] And when we were discussing about the lecture four, we provided you some examples from the
[09:13] BMW company what exactly they are doing in branding how customers they are
[09:19] identifying the BMW products and services within the market then data
[09:26] marketing tactics this is a lecture 3 okay you can take information from
[09:32] lecture 3 and we have some information in lecture 2 and lecture 3 the [uncertain: digital / Data]
[09:37] marketing [uncertain: strategy / Strategies] so in this section data marketing tactics you need to find
[09:42] out what data marketing channel and tactics have you chosen to reach your
[09:46] target audience how do you plan to leverage social media content marketing
[09:50] search engine optimization and other digital platforms to engage with
[09:55] customers so in this section you basically have to add all of the
[09:59] information related to your digital marketing strategies and we cover [uncertain: data / digital]
[10:05] marketing strategies in lecture 2 and lecture 3 so you can just download the
[10:09] lecture and the seminar slides and the mini case studies from lecture two and
[10:13] lecture three and you can take the information you can look at the
[10:18] examples and then connect the examples and resources with your poster and how
[10:24] you can add the information based on your company in this section then we
[10:28] have sales strategies what sales channels and techniques will you employ
[10:33] to drive revenue and customer acquisition have you outlined the sales
[10:37] process including lead generation prospecting and conversion strategies. We discuss about the KPIs
[10:43] and the metrics in week four. Okay so in week four we have information about the selling techniques,
[10:53] how you're going to close the sales, how you're going to finalize the deal based on different
[10:59] sales strategies. So we have urgency sales strategy, we have closed sales strategy,
[11:08] we have four or five important sales strategies. So if you just go back to a week four resources,
[11:17] you can find this information. So download the week four resources and week four resources
[11:23] in sales strategies, you can find some information how you're going to close the sale.
[11:29] Then you can find some information about the KPIs and metrics as well in terms of your conversion strategies.
[11:38] Then in terms of budgeting and resource allocation, the section 8, you need to provide the information about your resources first.
[11:47] What important resources you're going to use in your marketing plan to achieve your goals and objectives.
[11:55] and based on your resources what basically budget and how much budget you are going to allocate to
[12:04] each resource and you can find all of the information in week four resources as well so
[12:12] [uncertain: look / that] we we have a connection of the weekly resources so you are taking some information
[12:17] from week two and week three resources and you're adding in section six digital marketing tactics
[12:24] Then week four, which is basically your sales campaign and the sales strategies, the marketing plan. So you're taking some information from week four resources and you're adding in section seven and in section eight.
[12:46] Then we have section nine. It's all about your measurement and evaluation. How are you going to make sure that whatever the budget and whatever the resources you have allocated for your marketing plan, how are you going to achieve all of those things?
[13:00] Okay, so you need to work on your KPIs and metrics.
[13:04] How will you track and analyze the performance of your marketing campaign?
[13:08] So remember in week five we were discussing about the overall marketing plan and within the marketing plan you
[13:15] have to cover so much so many important things.
[13:19] You have steps, you have stages. So when you when you're planning to
[13:24] apply all of the stages in your marketing plan, what is the result? Have you achieved all of the steps?
[13:29] Have you achieved your goals? Have you achieved your objectives? So for that
[13:37] thing you need to work on measurement and evaluation stage. So what metrics and
[13:42] KPIs will you use to measure the success of your marketing strategy? How will you
[13:47] track and analyze the performance of your marketing campaigns? So this section
[13:53] is all about your metrics and KPIs and if you can just go back to the [uncertain: week five / (nothing)]
[13:58] week four resources the last slide will be the measurement and evaluation and you can find the
[14:04] example of BMW over there how basically they have worked on different KPIs what are the different
[14:11] key performing indicators what exactly they have to achieve in their marketing strategy in their
[14:17] overall marketing plan so all of the goals and objectives you can find in KPIs and the metrics
[14:22] how they are basically achieving all of the KPIs, what strategies, what tactics they are using to
[14:28] achieve all of their KPIs. Then the last one is basically your own reflection or you can say
[14:38] your own judgment, your own research, the creativity and innovation in your business,
[14:45] in your marketing plan. So have you demonstrated creativity and innovation in your marketing
[14:50] approach is there something new and whatever we have discussed from whatever we have discussed in
[14:56] week one week two three four and five is there any new marketing strategy you have used how have you
[15:02] incorporated new and emerging trends in your marketing strategy including ai personalization
[15:09] [uncertain: omni / only] channel [uncertain: euro / the auto] marketing subscription and revenue model so the subscription and the revenue
[15:15] model we have covered the elements in week five okay so in this creativity and innovation you
[15:22] need to cover all of the topics so in week one we discuss about the new approaches and the
[15:30] emerging trends in marketing okay remember we discussed about the [uncertain: omni / only] sale we discussed about
[15:35] the ai personalization neuro marketing etc etc so from week one resources you can add some of the
[15:42] important elements and you need to provide some examples how your company is using all of these
[15:48] new emerging trends. Then the week two and week three was all about the personalization, the
[15:56] consumer behavior. Then we discuss about the [uncertain: data and / digital] marketing strategies and you can add
[16:03] the information from week two and week three resources in your poster. And then the week four
[16:09] was all about the marketing plan so this assignment is basically related to the
[16:16] week [uncertain: before / four] topic the marketing plan so you need to create a marketing plan for
[16:22] the existing business or the new business and the week five was all about
[16:26] and the subscription and the revenue model so you are basically taking the
[16:33] information from all of the weekly resources all of the concepts all of the
[16:38] emerging trends and you're adding in your poster. So the last one we will see and the alignment
[16:43] with business objectives. How does your marketing strategy now you have completed the marketing
[16:48] strategy you have presented your marketing strategy. How does your marketing strategy
[16:52] align with the overall business goals and objectives? Okay, have you considered the long
[16:57] term sustainability and growth potential of your marketing initiative? So whatever you have added
[17:02] in your marketing plan based on the five topics okay so do we have any long-term sustainability
[17:11] and growth potential based on your marketing plan so whatever you're going to present it's not going
[17:17] to be for like short period of time they must have a sustainability and your marketing plan
[17:23] must have a long-term impact on the business in terms of the profitability as well
[17:31] So what exactly we are looking in your presentation in your poster? Is the poster visually appealing
[17:39] and well organized and easy to understand? Have you effectively communicated your overall
[17:46] marketing strategy through examples, visuals, graphics and text? If [uncertain: applicable / apply cable] cite all your
[17:53] sources in the poster. Use only reliable and credible references. Include a reference list
[17:59] at the end. Again, it's not mandatory, but if you're taking some information from internet,
[18:06] if you're using any statistical information, and if you're doing any research, okay, then you can
[18:11] just take some references and cite them in your poster, and then add the end reference list as
[18:19] well. Incorporate and draw relevant graphs and tables to support your content, and these will
[18:24] enhance the visual appeal and clarity of your work. So if you have all of these things in your
[18:31] poster and if you have covered all of the five topics elements, all of the five topics concepts
[18:38] in your poster and if you have explained all of the things properly during the presentation with
[18:47] examples okay because in your posters I can suggest you only add some bullet points
[18:54] download the Tesla case study from week four resources and see how they have basically
[19:01] added the information in their marketing plan okay and follow the steps okay you can add bullet
[19:09] information in your poster but when you're presenting your poster just try to explain
[19:15] the things with examples and when you're working on all of these things when you're following the
[19:21] assignment brief and when you're following the instructions then it means you're going to present
[19:27] your poster in an organized way and in a well organized manner and then we will give you the
[19:35] marks accordingly okay assessment schedule we have sent you the list okay your tutors they have
[19:44] already sent you the list so first week group presentations we will start in 4th June 2025
[19:51] which is [uncertain: venus day / Wednesday] and the second week group presentation 11th june 2025 which is again
[19:57] [uncertain: venus day / Wednesday] so if you have any questions regarding your groups for the second week we will give you
[20:03] some time in in the next week in this week tutorial so after the presentation you can
[20:11] discuss the things with your tutor and if you have some changes in your groups i'm just only
[20:17] talking about the secondary group presentations. So if you want to change the group, if you have any
[20:23] conflicts, we are here to help you guys and you can discuss your group things in this week's
[20:29] tutorial. So the important thing is the length. You need to present your poster for 15 minutes,
[20:38] okay, and then plus five minutes. So altogether it's going to be like 20 minutes,
[20:43] okay because we received some requests from the students because we have six
[20:48] tutorials from nine to five o'clock Wednesday and some of the students they
[20:55] said and they have like maximum six students in one [uncertain: group / drop] so just try to
[21:01] give us more time to explain the things so based on your things request we
[21:07] decided to increase the time and now the total time is 15 minutes only for your presentation
[21:15] and five minutes for the q a session uh the overall grading uh the weightage from uh 100
[21:23] percent is 40 percent because 60 is your video vlog which is your assignment too
[21:28] so 40 for this overall weightage is 40 but we are going to give you the marks from 100 okay
[21:34] So 80% grading for the poster content and 20% for your presentation.
[21:43] And the submission deadline is 12th June 2025.
[21:48] And once you're going to submit your poster from your individual account, it's going to be a same poster, but from your own individual account.
[21:57] and just take a picture and a clear picture okay crop it properly and then upload it to Moodle and
[22:07] then after 15 days we will give you the feedback like within 15 days we will give you the feedback
[22:13] and after 15 working days you will be able to find your grades and we will give the same grade for
[22:21] the whole group okay so please try to work together in a group because this is a group task
[22:27] and we will give you the same marks uh for for all of the group members okay so same marks for
[22:33] all of the group members um that's it um it's for like a brief session to just give you the brief
[22:40] overview what you have to add in your poster presentation hand-drawn poster presentation
[22:46] so thank you very much and attend your tutorials uh this week and obviously the next week as well
[22:51] for the group poster presentation uh you have my email address you have email address of your tutor
[22:57] dr kazi uh if you have any issues if you're not clear about anything if you have any misunderstanding
[23:04] about your groups and if you have any conflicts uh just try to send us the email and we will
[23:10] definitely helps you guys all right thank you very much guys see you this week Wednesday

## Disagreement register

Each row is one `[uncertain: …]` marker. The tie-break column shows the large-v3 words in a window of about 2.5 s before to 3 s after the timestamp; it is a third machine reading, not a verification.

| Time | Primary (large-v3-turbo) | Cross-check (medium.en) | Tie-break window (large-v3) |
|---|---|---|---|
| 01:11 | poster | processor | is what you need to include in your poster presentation. I've |
| 02:14 | (nothing) | page | So the presentation will be delivered in front of the class. Yes, you need to present your poster |
| 04:26 | and group | Nkruv | Okay, just try to add the name of the group member. Well, it's not mandatory, |
| 07:55 | market | (nothing) | did you segment and prioritize your target market so based on which segmentation you |
| 09:37 | digital | Data | in lecture two and lecture three the digital marketing strategies so in this section digital marketing |
| 09:37 | strategy | Strategies | and lecture three the digital marketing strategies so in this section digital marketing tactics |
| 10:04 | data | digital | strategies and we cover digital marketing strategies in lecture 2 and lecture 3. |
| 12:12 | look | that | week four resources as well. So look, we have a connection of the weekly resources. |
| 13:57 | week five | (nothing) | And if you can just go back to the week five, week four resources, the |
| 15:09 | omni | only | personalization, omni-channel, euro marketing, subscription and revenue model? |
| 15:10 | euro | the auto | omni-channel, euro marketing, subscription and revenue model? |
| 15:33 | omni | only | marketing. Okay, remember, we discussed about the Omni sale, we discussed about the AI personalization, |
| 16:00 | data and | digital | we discuss about the digital marketing strategies and you can add |
| 16:16 | before | four | to the week four topic the marketing plan so |
| 17:52 | applicable | apply cable | text? Next, if applicable, cite all your sources in the poster. Use only |
| 19:52 | venus day | Wednesday | uh 2025 uh which is venice day and the second week group presentation 11th june 2025 |
| 19:57 | venus day | Wednesday | june 2025 which is again venice day so if you have any questions regarding your |
| 20:59 | group | drop | six students in one group so just try to give us more time to explain |

## Passages where the models agree but the text is doubtful

These are not marked in the transcript because the primary and cross-check readings agree. A listener should check them.

- 09:21–09:46: all three models write "data marketing tactics" at 09:21–09:26 and "data marketing channel" at 09:41; at 09:37–09:41 the primary and cross-check write "data marketing tactics" and the tie-break model "digital marketing tactics". The slide on screen (`w06-lecture` s6) reads "Digital Marketing Tactics" and "What digital marketing channels". The speaker may be saying "digital"; not established.
- 15:33: marked `[uncertain: omni / only]`; the next word is "sale" in all three models (tie-break: "Omni sale"). The term intended is not established.
- 20:17: primary and cross-check write "secondary group presentations"; the tie-break model writes "second week group presentations".
- 22:57: all three models write the tutor's name as "Kazi" ("Dr. Kazi"). Spelling and identity are unverified.
- 21:28: "your assignment too" (primary) / "your assignment too" (cross-check) / "your assignment to" (tie-break); the speaker is taken to mean "assignment two", which is not established by the audio models.
