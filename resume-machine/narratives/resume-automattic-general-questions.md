https://automattic.com/work-with-us/job/experienced-software-engineer/

---

# What’s motivating you to explore an engineering role at Automattic and why now?

I’m drawn to Automattic for three reasons: its commitment to open source, its culture of kindness, and its careful, human‑centered approach to AI.

Open source aligns with my values. As a cofounder of Kalamazoo Collective Housing and an active participant in housing, food, and arts cooperatives, I’ve seen how co‑ownership and consensus‑based governance produce transparent decision making and shared accountability. Those structures intentionally allocate resources and opportunities so members can contribute, learn, and grow — the same outcomes I value in open‑source communities.

Kindness sustains inclusion. Cooperatives succeed because members support one another, elevate quieter voices, and make space for diverse perspectives. Automattic’s creed to show respect and empathy mirrors that practice; a culture of mutual support enables honest feedback, thoughtful collaboration, and real shared ownership.

AI should amplify human creativity. I want to work on technology decisions that enhance people’s capabilities rather than replace judgment. Automattic’s measured adoption of large language models suggests thoughtful stewardship of these tools, and that clarity makes now the right time for me to contribute.

---

# When have you felt happiest at work? And when have you felt the least fulfilled? We’d love to understand the kinds of work, environments, or challenges that help you thrive – and what tends to have the opposite effect.

I am most fulfilled when:

- **Solving meaningful problems.** I enjoy untangling practical challenges that improve people's day‑to‑day experiences.

- **I have clear goals and impact metrics.** I thrive when success is measurable and we know what defines impact.

- **My team invested in our work.** Teams that understand why projects matter and align short‑term goals with long‑term value energize me.

- **In a culture of high trust and mutual support.** I flourish where contributions are valued, people are respectful, and collaboration is calm and constructive.

- **I have opportunities to learn and build.** I value creating useful products, meeting new people, and experimenting with emerging tech to stay curious and grow.

---

# Which part of the Automattic Creed resonates most with you, and why? If you have a story or example where this principle shaped your work, we’d love to hear it.

"I am more motivated by impact than money, and I know that Open Source is one of the most powerful ideas of our generation."

Open source resonates most with me because it expands capacity, grants ownership, and preserves choice for users.

Open source expands capacity for the underfunded. Community‑maintained tools let small organizations access infrastructure they could not otherwise afford.

That access matters, but ownership matters too. Open source gives users the ability to inspect, modify, and control their tools so software becomes an asset rather than a rented service.

Ownership preserves choice. When code is open, organizations can switch providers, avoid lock‑in, and resist opaque pricing or extractive licensing.

Because of these principles, I oppose an extraction‑first ethos. Sustainable impact comes from empowering users, not from maximizing short‑term revenue per client.

At Boiling Pot Media I built on WordPress, prioritized self‑service, and used clear pricing so clients could own and maintain their sites. I later closed the agency to focus on engineering that contributes to open communities and builds tools that serve people.

---

# Tell us about a project or piece of work you’re especially proud of – from any point in your career. What made it great? What was your role, and what parts were you personally responsible for? We’d love to hear about any architectural or technical decisions, trade-offs, and challenges you had to navigate along the way.

At GOOP I led the rollout of a self‑service CMS that removed a persistent bottleneck between Editorial and Engineering. When I arrived, editors were designing posts in Figma and engineering was rebuilding each design by hand. That workflow was slow, costly, and left no room for higher‑impact work.

Earlier attempts to introduce self‑service tools had failed because editors felt excluded and the tools didn't match their process. To avoid the same mistake I spoke with staff across departments and listened for the real needs and constraints.

We implemented a component‑based system built on ACF Flexible Content. The components give editors clear, simple controls while preserving the design flexibility they need. Behind the scenes the implementation uses pragmatic WordPress/PHP patterns and modular editor components so the codebase stays maintainable.

Within three months the editorial team adopted the system and the Figma→code handoff disappeared. Engineering reclaimed most of the time previously spent on article builds and could focus on higher‑value projects. The change made the content workflow faster, more reliable, and easier to maintain.

---

# What’s the most recent idea, book, blog post, or talk that changed how you think about your craft? What shifted for you, and how has it shaped the way you build, collaborate, or make decisions?

I recently read "Sleep‑time Compute: Beyond Inference Scaling at Test‑time" (Kevin Lin et al., arXiv:2504.13171v1). The paper proposes precomputing reasoning over persistent context during idle periods so queries can be answered with less test‑time compute and lower latency.

The approach improves work‑time accuracy. By doing heavy reasoning during idle periods, the system delivers better answers when a query arrives.

It also cuts real‑time compute and cost. Shifting work offline reduces test‑time tokens and can lower demand for hardware, energy, and water.

Beyond technical gains, it supports healthier work rhythms. If expensive computation can happen while systems are idle, engineers and users face less pressure to run long, intense sessions.

Finally, it resonated on a personal level. Stepping away from a problem often lets subconscious processes work in the background. Sleep‑time compute mirrors that habit and gives it a concrete, technical benefit.

---

# What’s a controversial or unpopular opinion you hold about software engineering, and why? This could be about tools, practices, philosophies – anything where your take might challenge conventional wisdom. We’re interested in how you think, not whether we agree.

Documentation is a crucial feature of a healthy repository.

This is not a radical idea on paper, but in practice documentation is often neglected. Teams inherit outdated guides, documentation goes unused, or writing docs feels like a chore. Good documentation requires time and attention, and people become cynical when that work isn't valued.

Today, neglect is harder to excuse. Tools like phpDocumentor and TypeDoc, paired with agentic AI, make generating and maintaining accurate docs far easier than before.

Documentation is leverage, not bureaucracy. Clear docs speed onboarding, reduce context switching, and make pair‑programming with LLMs far more effective. They preserve knowledge when staff changes and make codebases more resilient.

I treat documentation as a product feature: I document intent, examples, and maintenance notes, and I invest in automation and review so docs stay accurate and discoverable.

---

# Tell us about a time you strongly disagreed with someone on your team and how you worked through it. We'd love to understand how you approach collaboration and conflict, especially when values or technical perspectives differ.

I don't have a single, dramatic showdown to share. I surface disagreements early and with curiosity.

My approach is simple. I ask why, assume good intent, and focus on the problem rather than the person. I explain my reasoning so others can respond to the evidence. I am willing to change my mind when shown better information.

A concrete example: at GOOP, Editorial wanted complete design freedom while Engineering needed maintainable structures. I ran stakeholder interviews to clarify actual needs. We designed a component system that preserved editorial flexibility and kept the codebase sustainable.

Ultimately, I prefer working with people who disagree in good faith. Thoughtful collaboration matters more to me than being right.

Steve Deckert
Strategic Partnerships, WooCommerce @ Automattic
