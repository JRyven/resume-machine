https://automattic.com/work-with-us/job/solutions-engineer-wordpress-vip/

# Tell us about a technical sale that you won (or helped win) that involved you delivering a custom or complex demo.

I'd like to tell you about a technical sale I secured while running my agency, Boiling Pot Media.\n\n

Raybend, a sump-pump manufacturer, inquired about hosting. The company that had created their WordPress website was no longer available.\n\n

Their website was simple—a limited frontend for brand information and a basic pump serial number tracking plugin. They gave me administrator access so I could review the setup before I visited.\n\n

When I arrived for our on-site meeting, I was greeted by two stakeholders: Joe—owner and no-nonsense businessperson—and Dagne, his right hand. During introductions I noted that I may have installed some of Raybend's pumps in the past. I worked with my dad - a master plumber - often before and throughout college. I have a wide range of professional experience and find sharing that information makes clients more likely share a detailed account of their work. People who swing a hammer like to know that you can swing a hammer, too. After an impatient handshake, Joe left Dagne to bring me on a tour of the facility. Dagne did a little damage control, explaining that Joe's head was always in two places at once.\n\n

Dagne walked me through their back office, engineering room, and manufacturing floor, explaining how Raybend stood apart from their competition by physically testing each pump against predefined performance criteria. Pumps that fail don't get sold.\n\n

During the floor tour, I asked questions. What was the significance of the PSI and amperage range tests? How did operators know if a pump passed or failed? What did "pump head" mean? Dagne had a lot of technical knowledge to impart. I asked how much time it took to assemble a unit, and Dagne illustrated common points of friction for the assembly line. At least weekly, she or Joe would run a stopwatch to benchmark assembly speed. I remarked that when I worked at a commercial greenhouse, the owner would run a stopwatch on the assembly line, too. But if we knew there was a stopwatch on the floor, we were going to double our effort to avoid getting in trouble so he could never get a true measurement of throughput.\n\n

My impression is that Dagne observed and appreciated the combination of focus and curiosity I brought to understanding their operation.\n\n

Dagne shared that they had contacted several other companies in the region that had expressed little interest in Raybend. I imagined disinterested voices over tinny phone lines saying, "Yeah, sure Dagne, your website isn't a big deal, we can host it no problem."\n\n

Joe wanted a contact who understood his company, she said. I had requested to visit—I was curious. I showed up on time—I kept a commitment. Joe liked those things.\n\n

Our tour ended at Joe's office. It was apparent they had decided to give me the hosting contract. I had provided a clear sales sheet on my service and commitment. Dagne had asked several questions on the tour—mostly about disaster recovery—and gave Joe a CliffsNotes review.\n\n

Joe wasn't interested in talking about hosting anymore. He appeared content that I had satisfied Dagne. Half his attention was spent deleting emails.\n\n

I had saved some thoughts that I wanted to share with both of them present.

First, I suggested that they leverage the existing plugin data to calculate the average time it took to assemble a pump. The serial number tracking system was a custom post type with a custom field. Calculating pumps-per-hour was as simple as exporting the post data and setting up a spreadsheet computation. Of course, that kind of reporting feature could also be built into a dashboard on the website.\n\n

The second suggestion was to configure the serial number field to automatically fill the next serial number. Operators were typing ten-digit numbers with leading zeros ("0000069218"), which looked time consuming. "And error prone," Dagne added. She explained that when errors occurred—duplicate serial numbers, transposed digits—she or another office staff member would need to log into WordPress, find the errors, and manually correct them. It was a massive time-saver she was describing, which always equates to money.\n\n

Joe wasn't multitasking anymore. What they disclosed next indicated that Joe believed I might have the skillset to help him complete a vision he'd set aside. The previous developer had not impressed Joe, and he'd shelved his ideas, unclear on who could build what he really wanted.\n\n

The feature he envisioned would track unique performance metrics for each pump, the line operator who entered the data, retail price, warranty expiration date, produce QR code labels, feature several user roles, and offer the ability—without calling in a software engineer—to configure new metrics for additional pump models over time.\n\n

I outlined how I would approach the project using WordPress post types, taxonomies, and custom fields to create a robust unit tracking system. When they asked about comprehensive tracking capabilities, I explained how these tools could scale to meet their needs.\n\n

Two weeks later, I brought my laptop to our next meeting and demoed bootstrapped pages. I had sent Dagne two messages during that time to let her know I was on track. The demo included a login and authentication flow, the data entry workflow optimized for both keyboard and touchscreen operators, and the raw data capture and export system.\n\n

Joe was most concerned to see that the site would offer his company the ability to expand pump model coverage and adjust test parameters without developer intervention. Dagne was most concerned about the level of complexity for managing these same details. I had chosen to make pump model a custom taxonomy with custom fields. Both were pleased to see the logical admin structure.\n\n

Most of their thoughts after addressing the admin experience pertained to the UX for line operators: login screen, data entry screen, techniques for "undoing" an accidental record creation, automated logout, large field fonts and submission buttons, and error logging. I walked through the UX, highlighting choices I had made to ensure that operators could navigate the data entry rapidly while validating values to prevent errors.\n\n

Their concerns about warranty and support terms were quickly resolved—my hosting package included monthly "use-it-or-lose-it" support hours, and we came to mutual confidence quickly.\n\n

The contract amounted to 5% of my revenue that year.\n\n

I built the system collaboratively with one of my staff, a strategic hire to fill out my agency's front-end capabilities. I handled the backend engineering while he ensured a smooth workflow for triggering the print dialogue for serial number labels with QR codes. Raybend installed sticker-printers at each assembly line to print labels on demand. We divided backend and frontend tasks and reviewed each other's work. One minor constraint we navigated: Joe wanted the print sequence to include two modals, but we had agreed to use the browser's native print feature, which required a single modal sequence.\n\n

The following year, we alleviated Raybend's call burden by building a user role and pump data lookup for their resellers, giving them self-service access to pump warranty data.\n\n

The site has logged metrics for more than one million pumps. After I closed my business and referred all my clients to a former employee, Raybend insisted they would only work with me.\n\n
