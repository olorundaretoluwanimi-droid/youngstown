#!/usr/bin/env python3
"""The script, line by line → audio/lines.json (for the AI33 narrator) and script.md (readable).
Each entry: id, chapter, text (spoken, numbers as words), subs (caption lines, digits, one line each ≤ ~58 characters).
Told as a court case: the charge, ten parts on the docket, the verdict, then the viewer is the jury. Every fact is in FACTS.md.
Witness cards (W): a worker's own words appear on screen in silence — the narrator never speaks as a worker. 'hold' = seconds on screen.
Court documents (hot-line messages, the judges' words, testimony) are public record: the narrator reads them as documents."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = 'elevenlabs_0dPqNXnhg2bmxQv1WKDp'   # Storyteller Oxley (AI33 Pro / ElevenLabs)
C = []
def L(ch, i, spoken, *subs): C.append((ch, i, spoken, list(subs)))
WIT = {}
def W(ch, i, hold, **card): C.append((ch, i, '', [])); WIT[i] = dict(hold=hold, **card)

# ── the charge (cold open) ──
L('hook', 'h01', "On Monday, the nineteenth of September, nineteen seventy-seven, the union presidents at Youngstown Sheet and Tube were told to come to a meeting at ten in the morning.",
  "On Monday, 19 September 1977, the union presidents", "at Youngstown Sheet and Tube were told", "to come to a meeting at ten in the morning.")
L('hook', 'h02', "A company manager handed them a statement and read it aloud. Most of the Campbell Works was closing. About five thousand people would lose their jobs.",
  "A company manager handed them a statement and read it aloud.", "Most of the Campbell Works was closing.", "About 5,000 people would lose their jobs.")
L('hook', 'h03', "One of the union men interrupted him with a question.", "One of the union men interrupted him with a question.")
W('hook', 'w01', 5.2, q=['“Are you cutting the cord?', 'Are they done?”', '', '“Yes.”'], who='Ed Mann · and the company’s answer',
  role='PRESIDENT, LOCAL 1462 · 19 SEPTEMBER 1977', src='AS RECOUNTED TO THE NLRB · STAUGHTON LYND, THE FIGHT AGAINST SHUTDOWNS (1982)')
L('hook', 'h04', "Youngstown, Ohio. In nineteen thirty, a hundred and seventy thousand people lived here. In twenty twenty, about sixty thousand.",
  "Youngstown, Ohio. In 1930, 170,002 people lived here.", "In 2020, 60,068.")
L('hook', 'h05', "Two years after that Monday, when a second steel company said it was leaving too, the steelworkers of this town did something almost no town had tried.",
  "Two years after that Monday, when a second steel company", "said it was leaving too, the steelworkers of this town", "did something almost no town had tried.")
L('hook', 'h06', "They took the company to federal court. And they asked a judge to rule that a town has a right to the mill it built its life around.",
  "They took the company to federal court.", "And they asked a judge to rule that a town has a right", "to the mill it built its life around.")
L('hook', 'h07', "Tonight, you'll hear that case. The charge. The evidence. The witnesses. The company's defence. And the verdict. Then you decide.",
  "Tonight, you'll hear that case. The charge. The evidence.", "The witnesses. The company's defence. And the verdict.", "Then you decide.")
L('hook', 'h08', "This is for anyone who ever packed a lunch for a shift like that. This is Mill Town.",
  "This is for anyone who ever packed a lunch for a shift like that.", "This is Mill Town.")

# ── part 1 · opening statement ──
L('p1', 'a01', "Part one. The opening statement.", "Part one. The opening statement.")
L('p1', 'a02', "The Mahoning River runs south-east out of Warren, through Niles and Girard, through Youngstown, Campbell and Struthers, and on into Pennsylvania.",
  "The Mahoning River runs south-east out of Warren,", "through Niles and Girard, through Youngstown,", "Campbell and Struthers, and on into Pennsylvania.")
L('p1', 'a03', "People were making iron along this river by the early eighteen hundreds. There was coal in the hills, and limestone, and water.",
  "People were making iron along this river", "by the early 1800s.", "There was coal in the hills, and limestone, and water.")
L('p1', 'a04', "In nineteen hundred, a group of Youngstown men raised six hundred thousand dollars and started a company of their own. They called it the Youngstown Iron Sheet and Tube Company.",
  "In 1900, a group of Youngstown men raised $600,000", "and started a company of their own.", "They called it the Youngstown Iron Sheet and Tube Company.")
L('p1', 'a05', "It was a local company, run by local families. It would grow into one of the biggest steelmakers in America.",
  "It was a local company, run by local families.", "It would grow into one of the biggest steelmakers in America.")
L('p1', 'a06', "In nineteen oh one, the Ohio Works, on the west side of town, began making steel for a new giant: the United States Steel Corporation.",
  "In 1901, the Ohio Works, on the west side of town,", "began making steel for a new giant:", "the United States Steel Corporation.")
L('p1', 'a07', "In nineteen eighteen, U.S. Steel added the McDonald Works, a few miles upriver.",
  "In 1918, U.S. Steel added the McDonald Works,", "a few miles upriver.")
L('p1', 'a08', "And on the twentieth of September that year, at the Brier Hill Works, a girl named Mary Jeannette Thomas lit a brand-new blast furnace.",
  "And on 20 September that year, at the Brier Hill Works,", "a girl named Mary Jeannette Thomas", "lit a brand-new blast furnace.")
L('p1', 'a09', "They named it after her. Jeannette. Everyone in town called it Jenny.",
  "They named it after her. Jeannette.", "Everyone in town called it Jenny.")
L('p1', 'a10', "Four great mills along one river, and more besides. And around them, a city grew.",
  "Four great mills along one river, and more besides.", "And around them, a city grew.")
L('p1', 'a11', "By nineteen thirty, Youngstown had a hundred and seventy thousand people. Many had crossed an ocean to work in steel.",
  "By 1930, Youngstown had 170,002 people.", "Many had crossed an ocean to work in steel.")
L('p1', 'a12', "So here is the first thing the jury should ask. What did the mills give this town? And what did the town give back?",
  "So here is the first thing the jury should ask.", "What did the mills give this town?", "And what did the town give back?")

# ── part 2 · exhibit A: what the town built ──
L('p2', 'b01', "Part two. Exhibit A. What the town built.", "Part two. Exhibit A. What the town built.")
L('p2', 'b02', "In nineteen forty-four, the government sent a film crew to Youngstown to show the country how steel was made for the war.",
  "In 1944, the government sent a film crew to Youngstown", "to show the country how steel was made for the war.")
L('p2', 'b03', "They called the film Steel Town. These are the people they found.", "They called the film Steel Town.", "These are the people they found.")
L('p2', 'b04', "Italians on Brier Hill. Slovaks, Hungarians, Greeks, Poles, and many more. And Black families who had come north from the South.",
  "Italians on Brier Hill. Slovaks, Hungarians, Greeks, Poles,", "and many more. And Black families who had come north", "from the South.")
L('p2', 'b05', "The work was hot, loud and dangerous. Men stood a few feet from molten iron for eight hours at a time.",
  "The work was hot, loud and dangerous.", "Men stood a few feet from molten iron for eight hours at a time.")
L('p2', 'b06', "They fought for a union, and in the summer of nineteen thirty-seven, people were killed in Youngstown in that fight. But the union came.",
  "They fought for a union, and in the summer of 1937,", "people were killed in Youngstown in that fight.", "But the union came.")
L('p2', 'b07', "And with it, a mill job that paid for a house. A car. A summer week at the lake. Children who went to college.",
  "And with it, a mill job that paid for a house. A car.", "A summer week at the lake. Children who went to college.")
L('p2', 'b08', "By nineteen fifty, Sheet and Tube alone employed about twenty-seven thousand people.",
  "By 1950, Sheet and Tube alone employed about 27,000 people.")
L('p2', 'b09', "Years later, one of those steelworkers described the job in a single sentence.", "Years later, one of those steelworkers", "described the job in a single sentence.")
W('p2', 'w02', 5.6, q=['“Every day you put your life', 'on the line when you went', 'into that iron house.”'], who='Ed Mann',
  role='BRIER HILL STEELWORKER · SPEAKING IN 1980', src='SPEECH, 28 JAN 1980 · LYND, THE FIGHT AGAINST SHUTDOWNS (1982)', img='st_worker')
L('p2', 'b10', "This was the bargain. The town gave the mills its sons, its daughters, its air and its river. The mills gave the town a living.",
  "This was the bargain. The town gave the mills its sons,", "its daughters, its air and its river.", "The mills gave the town a living.")
L('p2', 'b11', "But a bargain needs two sides. So who owned all this?", "But a bargain needs two sides.", "So who owned all this?")

# ── part 3 · exhibit B: the merger ──
L('p3', 'c01', "Part three. Exhibit B. The merger.", "Part three. Exhibit B. The merger.")
L('p3', 'c02', "In nineteen sixty-nine, Youngstown Sheet and Tube merged with the Likes Corporation, a shipping company from New Orleans.",
  "In 1969, Youngstown Sheet and Tube merged with", "the Lykes Corporation, a shipping company from New Orleans.")
L('p3', 'c03', "The decisions about Youngstown's biggest employer were now made a thousand miles away, by a company that did not make steel.",
  "The decisions about Youngstown's biggest employer were now", "made a thousand miles away,", "by a company that did not make steel.")
L('p3', 'c04', "The merger left Sheet and Tube carrying heavy debt. And the money that was spent on steel went mostly to the company's newer works near Chicago.",
  "The merger left Sheet and Tube carrying heavy debt.", "And the money that was spent on steel went mostly", "to the company's newer works near Chicago.")
L('p3', 'c05', "Meanwhile, the Campbell Works was getting old. Cheaper steel was arriving from Japan and Europe.",
  "Meanwhile, the Campbell Works was getting old.", "Cheaper steel was arriving from Japan and Europe.")
L('p3', 'c06', "In the summer of nineteen seventy-seven, the union men asked the managers whether the plant was in trouble. Under oath, later, they said the answer was: we'll make it.",
  "In the summer of 1977, the union men asked the managers", "whether the plant was in trouble. Under oath, later,", "they said the answer was: “We'll make it.”")
L('p3', 'c07', "Then came Monday, the nineteenth of September.", "Then came Monday, 19 September.")
L('p3', 'c08', "The statement said the company would move a major part of its steelmaking to Indiana Harbor, near Chicago. It said the cutback would require the lay-off or termination of approximately five thousand employees.",
  "The statement said the company would move a major part", "of its steelmaking to Indiana Harbor, near Chicago.", "The cutback would require the lay-off or termination",
  "of approximately 5,000 employees.")
L('p3', 'c09', "There had been no warning. There was no law that said there had to be.", "There had been no warning.", "There was no law that said there had to be.")
L('p3', 'c10', "Youngstown still has a name for that day. Black Monday.", "Youngstown still has a name for that day.", "Black Monday.")
L('p3', 'c11', "At Thanksgiving, a hundred and eighty-five clergy from across the valley signed a pastoral letter. It opened with one line.",
  "At Thanksgiving, 185 clergy from across the valley", "signed a pastoral letter. It opened with one line.")
W('p3', 'w03', 4.6, q=['“Our community was wounded', 'on September 19.”'], who='Pastoral letter',
  role='185 RELIGIOUS LEADERS OF THE MAHONING VALLEY · NOV 1977', src='QUOTED IN LYND, THE FIGHT AGAINST SHUTDOWNS (1982)')
L('p3', 'c12', "And then the people who signed it asked a question nobody had asked before. Could the town buy its own mill back?",
  "And then the people who signed it asked a question", "nobody had asked before.", "Could the town buy its own mill back?")

# ── part 4 · the witnesses ──
L('p4', 'd01', "Part four. The witnesses.", "Part four. The witnesses.")
L('p4', 'd02', "The first to come forward were churchmen. The Catholic bishop of Youngstown, James Malone. The Episcopal bishop of Ohio, John Burt.",
  "The first to come forward were churchmen.", "The Catholic bishop of Youngstown, James Malone.", "The Episcopal bishop of Ohio, John Burt.")
L('p4', 'd03', "They formed the Ecumenical Coalition of the Mahoning Valley, and they set out to reopen the Campbell Works, owned by its workers and its community.",
  "They formed the Ecumenical Coalition of the Mahoning Valley,", "and they set out to reopen the Campbell Works,", "owned by its workers and its community.")
L('p4', 'd04', "It would cost hundreds of millions of dollars. So they asked the town to show Washington that it meant it.",
  "It would cost hundreds of millions of dollars.", "So they asked the town to show Washington that it meant it.")
L('p4', 'd05', "In February nineteen seventy-eight, at a church service in Boardman, they opened the Save Our Valley campaign. People opened savings accounts that could one day become shares in the mill.",
  "In February 1978, at a church service in Boardman,", "they opened the Save Our Valley campaign.", "People opened savings accounts that could one day",
  "become shares in the mill.")
L('p4', 'd06', "By that November, there were four thousand, one hundred and thirty-eight accounts. Just over four million dollars.",
  "By that November, there were 4,138 accounts.", "Just over $4 million.")
L('p4', 'd07', "It was never going to be enough on its own. The plan needed federal loan guarantees. And for months, the town waited for Washington.",
  "It was never going to be enough on its own.", "The plan needed federal loan guarantees.", "And for months, the town waited for Washington.")
L('p4', 'd08', "On the twenty-ninth of March, nineteen seventy-nine, a steelworker named Len Balluck stood in front of the reporters.",
  "On 29 March 1979, a steelworker named Len Balluck", "stood in front of the reporters.")
W('p4', 'w04', 4.8, q=['“They threw 5,000 lives', 'on a human garbage pile.”'], who='Len Balluck',
  role='CAMPBELL WORKS STEELWORKER FOR 20 YEARS · 29 MARCH 1979', src='PRESS CONFERENCE · QUOTED IN LYND, THE FIGHT AGAINST SHUTDOWNS (1982)')
L('p4', 'd09', "The next morning, a letter arrived from the Commerce Department. The coalition's plan needed two hundred and forty-five million dollars in guarantees. The limit for any one company, the letter said, was one hundred million.",
  "The next morning, a letter arrived from the Commerce Department.", "The plan needed $245 million in guarantees.", "The limit for any one company, the letter said,", "was $100 million.")
L('p4', 'd10', "The answer was no.", "The answer was no.")
L('p4', 'd11', "The national steelworkers' union, in Pittsburgh, had its own strategy for the whole industry, and it kept its distance from the fight in Youngstown.",
  "The national steelworkers' union, in Pittsburgh,", "had its own strategy for the whole industry,", "and it kept its distance from the fight in Youngstown.")
L('p4', 'd12', "And by then, the second wave had already come. Sheet and Tube had been merged again, into a bigger company, and the Brier Hill Works was to close by the end of nineteen seventy-nine.",
  "And by then, the second wave had already come.", "Sheet and Tube had been merged again, into a bigger company,", "and the Brier Hill Works was to close by the end of 1979.")
L('p4', 'd13', "About fifteen hundred more jobs. By the end of the year, Brier Hill was silent.", "About 1,500 more jobs.", "By the end of the year, Brier Hill was silent.")
L('p4', 'd14', "That left one company in town still making steel. U.S. Steel. Was anyone still promising to stay?",
  "That left one company in town still making steel. U.S. Steel.", "Was anyone still promising to stay?")

# ── part 5 · exhibit C: the promise ──
L('p5', 'e01', "Part five. Exhibit C. The promise.", "Part five. Exhibit C. The promise.")
L('p5', 'e02', "U.S. Steel's Ohio and McDonald Works employed about thirty-five hundred people. And they could hear the news from down the river.",
  "U.S. Steel's Ohio and McDonald Works employed about 3,500 people.", "And they could hear the news from down the river.")
L('p5', 'e03', "The company had a telephone hot line its workers could call for news. Every message was recorded. Later, they would be read out in court.",
  "The company had a telephone hot line its workers could call", "for news. Every message was recorded.", "Later, they would be read out in court.")
L('p5', 'e04', "On the first of September, nineteen seventy-seven, eighteen days before Black Monday, the superintendent, Bill Ashton, recorded this: there are no immediate plans to permanently shut down either the Ohio Works or McDonald Mills.",
  "On 1 September 1977, 18 days before Black Monday,", "the superintendent, Bill Ashton, recorded this:", "“There are no immediate plans to permanently shut down", "either the Ohio Works or McDonald Mills.”")
L('p5', 'e05', "But he added: the continued operation of these plants is absolutely dependent upon their being profit-makers.",
  "But he added: “The continued operation of these plants", "is absolutely dependent upon their being profit-makers.”")
L('p5', 'e06', "So the workers set out to make them profitable. In February nineteen seventy-eight, a new superintendent took over. His name was Bill Kirwan.",
  "So the workers set out to make them profitable.", "In February 1978, a new superintendent took over.", "His name was Bill Kirwan.")
L('p5', 'e07', "That April, he had good news for the hot line. In March, for the first time in a long, long time, the Youngstown Works had earned a profit.",
  "That April, he had good news for the hot line.", "“In the month of March, for the first time in a long, long time,", "the Youngstown Works earned a profit.”")
L('p5', 'e08', "And he signed off like this. Keep up the momentum. Our future is what we make it.",
  "And he signed off like this:", "“Keep up the momentum — our future is what we make it.”")
L('p5', 'e09', "At the end of the year, he thanked every man and woman at the two mills. The goal for nineteen seventy-eight, he said, had been survival. The goal for nineteen seventy-nine was revival.",
  "At the end of the year, he thanked every man and woman", "at the two mills. The goal for 1978, he said,", "had been “survival.” The goal for 1979 was “revival.”")
L('p5', 'e10', "In June nineteen seventy-nine, U.S. Steel's chairman, David Roderick, said it on television. Simply stated, we have no plans for shutting down our Youngstown operation.",
  "In June 1979, U.S. Steel's chairman, David Roderick,", "said it on television: “Simply stated, we have no plans", "for shutting down our Youngstown operation.”")
L('p5', 'e11', "On the twenty-seventh of November, nineteen seventy-nine, a steelworker named Frank Georges bought a new house. Driving home from the bank, he heard the news on his car radio.",
  "On 27 November 1979, a steelworker named Frank Georges", "bought a new house. Driving home from the bank,", "he heard the news on his car radio.")
L('p5', 'e12', "U.S. Steel was closing the Ohio Works and the McDonald Works. Thirty-five hundred more jobs.",
  "U.S. Steel was closing the Ohio Works and the McDonald Works.", "3,500 more jobs.")
L('p5', 'e13', "On a freezing Monday in January nineteen eighty, the steelworkers met at the Local thirteen-thirty union hall. U.S. Steel's district headquarters was just down the hill.",
  "On a freezing Monday in January 1980, the steelworkers met", "at the Local 1330 union hall.", "U.S. Steel's district headquarters was just down the hill.")
L('p5', 'e14', "Ed Mann, whose own mill at Brier Hill was already gone, stood up and told the meeting where he was going.",
  "Ed Mann, whose own mill at Brier Hill was already gone,", "stood up and told the meeting where he was going.")
W('p5', 'w05', 5.4, q=['“Now, I’m going down that hill', 'and I’m going into', 'that building.”'], who='Ed Mann',
  role='PRESIDENT, LOCAL 1462 · 28 JANUARY 1980', src='SPEECH AT THE LOCAL 1330 HALL · LYND, THE FIGHT AGAINST SHUTDOWNS (1982)', img='st_crowd')
L('p5', 'e15', "Hundreds followed him. The door gave way. For several hours, the steelworkers held the building, and a banner hung from the upper windows: Keep Our Mills Open.",
  "Hundreds followed him. The door gave way.", "For several hours, the steelworkers held the building,", "and a banner hung from the upper windows:", "“Keep Our Mills Open.”")
L('p5', 'e16', "They had believed a promise. But can a promise like that hold up in court?", "They had believed a promise.", "But can a promise like that hold up in court?")

# ── part 6 · the trial ──
L('p6', 'f01', "Part six. The trial.", "Part six. The trial.")
L('p6', 'f02', "On the twenty-first of December, nineteen seventy-nine, the steelworkers had filed suit. Local thirteen-thirty, United Steel Workers of America, against the United States Steel Corporation.",
  "On 21 December 1979, the steelworkers had filed suit.", "Local 1330, United Steel Workers of America,", "against the United States Steel Corporation.")
L('p6', 'f03', "Their lawyer was Staughton Lynd, a historian turned labour lawyer. The case went to a federal judge in Cleveland, Thomas Lambros.",
  "Their lawyer was Staughton Lynd, a historian turned labour lawyer.", "The case went to a federal judge in Cleveland, Thomas Lambros.")
L('p6', 'f04', "The workers made two arguments. First: the company had made a promise, and they had kept their side of it.",
  "The workers made two arguments.", "First: the company had made a promise,", "and they had kept their side of it.")
L('p6', 'f05', "And second, an idea no American court had ever accepted. That after eighty years, the town itself had a claim on the mills.",
  "And second, an idea no American court had ever accepted.", "That after eighty years, the town itself", "had a claim on the mills.")
L('p6', 'f06', "In February, U.S. Steel told the court it would shut the mills sooner than planned. Judge Lambros called both sides in.",
  "In February, U.S. Steel told the court it would shut the mills", "sooner than planned. Judge Lambros called both sides in.")
L('p6', 'f07', "And on the twenty-eighth of February, nineteen eighty, the judge himself said something nobody in the room expected.",
  "And on 28 February 1980, the judge himself", "said something nobody in the room expected.")
L('p6', 'f08', "Everything that has happened in the Mahoning Valley has been happening for many years because of steel. Schools have been built, roads have been built.",
  "“Everything that has happened in the Mahoning Valley", "has been happening for many years because of steel.", "Schools have been built, roads have been built.”")
L('p6', 'f09', "It seems to me, he said, that a property right has arisen from this lengthy, long-established relationship.",
  "“It seems to me that a property right has arisen", "from this lengthy, long-established relationship.”")
L('p6', 'f10', "He ordered U.S. Steel to keep the mills open until the case was heard. And he moved the trial to Youngstown, close enough to Pittsburgh that the company's chairman could be made to testify.",
  "He ordered U.S. Steel to keep the mills open until the case", "was heard. And he moved the trial to Youngstown,", "close enough to Pittsburgh that the company's chairman", "could be made to testify.")
L('p6', 'f11', "The trial opened on the seventeenth of March, nineteen eighty. It lasted five days.",
  "The trial opened on 17 March 1980.", "It lasted five days.")
L('p6', 'f12', "The workers had made their case. Now, what would the company say for itself?", "The workers had made their case.", "Now, what would the company say for itself?")

# ── part 7 · the defence ──
L('p7', 'g01', "Part seven. The defence.", "Part seven. The defence.")
L('p7', 'g02', "U.S. Steel's answer was simple. The mills were losing money, and nothing the workers did could change that.",
  "U.S. Steel's answer was simple.", "The mills were losing money,", "and nothing the workers did could change that.")
L('p7', 'g03', "The company's president testified that the main cause was obsolescence. The Ohio Works still made its steel in open-hearth furnaces, a method most of the industry was leaving behind.",
  "The company's president testified that the main cause", "was obsolescence. The Ohio Works still made its steel", "in open-hearth furnaces,", "a method most of the industry was leaving behind.")
L('p7', 'g04', "Modern mills were moving to basic oxygen furnaces, electric furnaces, and continuous casters. Rebuilding Youngstown that way would cost hundreds of millions of dollars.",
  "Modern mills were moving to basic oxygen furnaces,", "electric furnaces, and continuous casters.", "Rebuilding Youngstown that way", "would cost hundreds of millions of dollars.")
L('p7', 'g05', "The chairman, David Roderick, was asked whether the Youngstown Works had been about breaking even in nineteen seventy-nine. The actual number, he said, was about a three-hundred-thousand-dollar loss, for the year to the end of October.",
  "The chairman, David Roderick, was asked whether the Works", "had been about breaking even in 1979.", "“The actual number was about a $300 thousand loss,", "as of the end of October, cumulative for the year.”")
L('p7', 'g06', "The workers pointed to the company's own figures. Count only the day-to-day costs of making steel, and the Youngstown Works came out more than thirty-two million dollars ahead for nineteen eighty.",
  "The workers pointed to the company's own figures.", "Count only the day-to-day costs of making steel, and the Works", "came out more than $32 million ahead for 1980.")
L('p7', 'g07', "But count everything, the equipment wearing out, the selling costs, the overheads, and the company's own projection for nineteen eighty was a loss of nine point four million dollars.",
  "But count everything — the equipment wearing out,", "the selling costs, the overheads —", "and the company's own projection for 1980", "was a loss of $9.4 million.")
L('p7', 'g08', "Same mills. Same year. Two honest ways of reading the books.", "Same mills. Same year.", "Two honest ways of reading the books.")
L('p7', 'g09', "And the promise? Read the hot line again, the company said. Every message tied the future to profit. If and when there will be a phase-out, Kirwan had said, depends on the plant's profitability.",
  "And the promise? Read the hot line again, the company said.", "Every message tied the future to profit.", "“If and when there will be a phase-out", "depends on the plant's profitability.”")
L('p7', 'g10', "Encouragement to a workforce, the company argued, is not a contract. And no law in Ohio or in America said a company could not close its own plant.",
  "Encouragement to a workforce, the company argued,", "is not a contract. And no law in Ohio or in America", "said a company could not close its own plant.")
L('p7', 'g11', "The workers had one more hope. Let us buy the mills, they said. Roderick told the court U.S. Steel would not sell to a competitor backed by federal money.",
  "The workers had one more hope. Let us buy the mills, they said.", "Roderick testified U.S. Steel would not sell", "to a competitor backed by federal money.")
L('p7', 'g12', "Both sides have spoken. Who's right?", "Both sides have spoken.", "Who's right?")

# ── part 8 · the verdict ──
L('p8', 'h11', "Part eight. The verdict.", "Part eight. The verdict.")
L('p8', 'h12', "On the morning of Friday, the twenty-first of March, nineteen eighty, the lawyers gave their closing arguments. Less than two hours later, Judge Lambros read his decision.",
  "On the morning of Friday, 21 March 1980,", "the lawyers gave their closing arguments.", "Less than two hours later, Judge Lambros read his decision.")
L('p8', 'h13', "On the promise, he found that the company had never promised to keep the mills open if the workers made them profitable. And that they had not been profitable.",
  "On the promise, he found that the company had never promised", "to keep the mills open if the workers made them profitable.", "And that they had not been profitable.")
L('p8', 'h14', "On the town's right to its mill, he wrote that the mechanism to recognize this new property right is not now in existence in the code of laws of our nation.",
  "On the town's right to its mill, he wrote:", "“The mechanism … to recognize this new property right", "is not now in existence in the code of laws of our nation.”")
L('p8', 'h15', "This court is not a legislative body, and can not make laws where none exist. This court can determine no legal basis for the finding of a property right.",
  "“This Court is not a legislative body", "and can not make laws where none exist.", "… This Court can determine no legal basis", "for the finding of a property right.”")
L('p8', 'h16', "The workers appealed. In July, the appeals court in Cincinnati agreed with the judge, and wrote why.",
  "The workers appealed. In July, the appeals court in Cincinnati", "agreed with the judge, and wrote why.")
L('p8', 'h17', "The former mill towns of New England, with their empty textile factory buildings, are monuments to the migration of textile manufacturers to the South.",
  "“The former mill towns of New England,", "with their empty textile factory buildings, are monuments", "to the migration of textile manufacturers to the South.”")
L('p8', 'h18', "Deciding what should happen when a plant closes, the court said, is the responsibility of the legislatures of the states, or of the Congress of the United States. Not of a judge.",
  "Deciding what should happen when a plant closes, the court said,", "is “the responsibility of the legislatures of the states", "or of the Congress of the United States.” Not of a judge.")
L('p8', 'h19', "The fires at the Ohio Works and the McDonald Works went out. In three years, Youngstown had lost about ten thousand steel jobs, and across the valley, tens of thousands more went with them.",
  "The fires at the Ohio Works and the McDonald Works went out.", "In three years, Youngstown had lost about 10,000 steel jobs,", "and across the valley, tens of thousands more went with them.")
L('p8', 'h20', "Over the years that followed, the furnaces came down, one after another. Jenny was the last. She was torn down in January nineteen ninety-seven.",
  "Over the years that followed, the furnaces came down,", "one after another. Jenny was the last.", "She was torn down in January 1997.")
L('p8', 'h21', "The workers lost their case. But did it change anything?", "The workers lost their case.", "But did it change anything?")

# ── part 9 · the jury ──
L('p9', 'j01', "Part nine. The jury.", "Part nine. The jury.")
L('p9', 'j02', "Judge Lambros had written that bills about plant closings were already pending on Capitol Hill. It took eight more years.",
  "Judge Lambros had written that bills about plant closings", "were already pending on Capitol Hill.", "It took eight more years.")
L('p9', 'j03', "In nineteen eighty-eight, Congress passed the WARN Act. Most large employers must now give sixty days' notice before a plant closing or a mass layoff.",
  "In 1988, Congress passed the WARN Act.", "Most large employers must now give 60 days' notice", "before a plant closing or a mass layoff.")
L('p9', 'j04', "Sixty days. On Black Monday, there had been none.", "60 days. On Black Monday, there had been none.")
L('p9', 'j05', "In nineteen ninety-two, the state opened a steel museum in Youngstown, in a building designed to look like a mill.",
  "In 1992, the state opened a steel museum in Youngstown,", "in a building designed to look like a mill.")
L('p9', 'j06', "In nineteen ninety-five, Bruce Springsteen named a song after the town, and put Jenny in it.",
  "In 1995, Bruce Springsteen named a song after the town,", "and put Jenny in it.")
L('p9', 'j07', "And in twenty twelve, a French steel company finished a six-hundred-and-fifty-million-dollar mill for steel pipe in the Brier Hill district, close to where Jenny stood. It was built for about three hundred and fifty jobs.",
  "And in 2012, a French steel company finished a $650 million", "mill for steel pipe in the Brier Hill district,", "close to where Jenny stood.", "It was built for about 350 jobs.")
L('p9', 'j08', "Youngstown today is a city of about sixty thousand. Fewer than in nineteen ten.", "Youngstown today is a city of about 60,000.", "Fewer than in 1910.")
L('p9', 'j09', "So here is the case. A company that said its mills were losing money, and had every legal right to close them.",
  "So here is the case. A company that said its mills", "were losing money, and had every legal right to close them.")
L('p9', 'j10', "And a town that had given those mills eighty years, and believed that ought to count for something.",
  "And a town that had given those mills eighty years,", "and believed that ought to count for something.")
L('p9', 'j11', "The law gave its answer in nineteen eighty. The question it could not answer is still here.",
  "The law gave its answer in 1980.", "The question it could not answer is still here.")
L('p9', 'j12', "Does a town have any right to the mill it built its life around?", "Does a town have any right", "to the mill it built its life around?")
L('p9', 'j13', "You've heard the case. What's your verdict?", "You've heard the case. What's your verdict?")
L('p9', 'j14', "Next time on Mill Town: Kenosha, Wisconsin.", "Next time on Mill Town: Kenosha, Wisconsin.")

os.makedirs(os.path.join(D, 'audio'), exist_ok=True)
json.dump([dict(id=i, chapter=ch, voice=V, text=sp, subs=su, **({'witness': WIT[i]} if i in WIT else {})) for ch, i, sp, su in C],
          open(os.path.join(D, 'audio', 'lines.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
names = {'hook': 'The Charge (cold open)', 'p1': 'Part 1 · Opening Statement', 'p2': 'Part 2 · Exhibit A: What the Town Built', 'p3': 'Part 3 · Exhibit B: The Merger',
         'p4': 'Part 4 · The Witnesses', 'p5': 'Part 5 · Exhibit C: The Promise', 'p6': 'Part 6 · The Trial', 'p7': 'Part 7 · The Defence',
         'p8': 'Part 8 · The Verdict', 'p9': 'Part 9 · The Jury'}
out, last = ['# What Happened to Youngstown? The Day the Steel Mills Closed — script', ''], None
for ch, i, sp, su in C:
    if ch != last: out += ['', f'## {names[ch]}', '']; last = ch
    out.append(f'**{i}** ' + (" ".join(su) if su else 'WITNESS CARD (silent): ' + ' '.join(x for x in WIT[i]['q'] if x) + f' — {WIT[i]["who"]}, {WIT[i]["role"]}'))
open(os.path.join(D, 'script.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
w = sum(len(sp.split()) for _, _, sp, _ in C); print(len(C), 'lines', w, 'words', f'~{w / 150:.1f} min of speech', 'chars', round(sum(len(sp) for _, _, sp, _ in C) * 1.0))
long = [(i, s) for _, i, _, su in C for s in su if len(s) > 66]; print('long caption lines:', long)
