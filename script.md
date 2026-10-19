# Voice-over: R/Pharma 2026

One piece, slide by slide. [Brackets] mark clicks. About 1,500 words: roughly 12 minutes spoken, closer to 16 with clicks and pauses.

---

**1 · Cover**

Hi everyone. I'm Afshin Mashadi-Hossein, and I lead the data science function at [company].

This work started with a question more than six years ago: why can't collaborating on data be as smooth as collaborating on code? Over the years, my colleagues and I put that idea into practice. Data as code delivered on its promise. But it also showed us something bigger: a chance to set a standard for how clinical data is stored.

So today brings the two together: a storage standard for clinical data, written and kept as code. Everything I'll show is open source, and I'll be clear about what ships today and what doesn't.

**2 · A stud is a promise**

Contrary to their reputation, standards, done well, work for agility and creativity, not against them. Hand anyone a random pile of Lego and they can start building right away. Why? Because a stud is a promise: a brick from 1958 still clicks into one you bought yesterday.

**3 · Pharma already has its stud** [click]

And our industry values data standards more than most. Move from one team to another, or one company to another, and you already know how adverse events are captured. That's CDISC.

**4 · We build data like a product** [5 clicks]

Not only that: pharma builds data much like a product. Each one has a purpose, [click] a specification, [click] a build, [click] QC, [click] and a release. [click] And after release…?

**5 · And then we save it to a folder**

And then we save this product, this labour of love, into a folder. [click] The same technology we use for cat pictures.

**6 · The bin** [2 clicks]

Back to the bricks. Every brick fits, so you can build the castle any time. [click] But once it's tipped into the bin, its pieces are mixed in with everything else. Which pieces were the castle? Which instructions built it? Has someone changed it since? Rebuilding it exactly gets hard. That's our data and the code that derived it, when nothing keeps them together. [click] CDISC made every brick fit. Nothing keeps a build's pieces together.

**7 · The usual fix** [click]

So, the usual fix: one more standard. Follow this list for every file, every time you save, code or data. [click] Every file. Every time. By hand. Problem solved… Nobody would do that. And even if they would…

**8 · Standards are like toothbrushes**

…as the saying goes, standards are like toothbrushes: everybody wants one, and nobody wants to use anybody else's. And using datom's toothbrush is no more pleasant.

**9 · So datom keeps its own** [click]

So datom does propose a standard, but it makes the standard its own business. No toothbrush sharing here. You write and you read; datom takes care of the list.

**10 · Beyond faster and cheaper** [4 clicks]

Great, you say: I don't have to worry about datom's standard. But what do I get from it? Think of the aim as what a modern stack makes possible, not the old way done faster and cheaper.

[click] Faster and cheaper is the same castle, sooner. That was a fine reason to come to open source, and it paid off. [click] Further starts when two sets meet. [click] It's the bridge no box ever shipped. [click] This isn't SAS, rewritten in R. That world ended in folders too.

**11 · The picture** [7 clicks]

So what can a more modern approach look like? Something like this.

Data arrives from the EDC. [click] A programmer writes code to spec, and it derives liver labs; the code is tracked right alongside the data. [click] Next month's data arrives as a new version, and every earlier version, and the work built on it, stays traceable. [click] A statistician just reads what they need, with minimal overhead. [click] A second study follows the same pattern, with its own reader.

[click] Now a new use case: a safety physician wants a dashboard that pools liver safety across both studies. The work already done is simply referenced, at exact versions: no duplication, and full provenance.

[click] Months go by. A new collaborator joins and works on the same code. Sources update and each study syncs, but the pooled set doesn't move… [click] until its programmer releases a new version, code and all. The dashboard follows that release.

Each role cares only about their own work. Study 1's programmer never needed to know a safety physician would come along. Yet the standard let the blocks click together into something new.

**12 · The same six months, in folders** [click]

Now imagine the same six months with folders and files, for data and for code. … So what did we do differently?

**13 · Data as code** [click]

Data as code is how we get there. Here's what I mean by it. Data as code means capturing a standard set of metadata about every data file: what it is, where it lives, how it relates to other files, and the code that made it. That metadata is small, so it can be kept, and treated, as code.

So it comes down to this: store each file in a standard way, register each one, document each registry as code, and let git do what it does best: track the code. [click] We didn't build a database.

**14 · The datom workflow** [9 clicks]

Here's how that works in datom.

[click] A programmer starts a project with one command. It creates the git repo and links it to a data store. [click] New data arrives, and a single sync stores the data and its record as code. [click] A second programmer joins the way they would any code project: they clone the repo. That brings the code, not the data. [click] Next month's snapshot has dm unchanged, a new version of lb, and a new table, ae. One more sync handles all three. [click] A reader reads any table, by version, with a single read.

[click] Raw EDC data is rarely what readers want, though. A programmer can compose derived data in a new project, started in product mode. [click] A sync there links to the tables in the study, importing them without copying anything. Writing it gives the first version of the set. [click] Then the programmer adds R code that derives a new table, liver_flags. One write records a second version of the set: pointers to its inputs, the code, and the new table, all recorded in git together, while the data itself sits in storage. [click] And a reader pulls the set by version, picks any member, and fetches it.

**15 · What you get, every time**

If you're still asking "so what?", this is the slide.

Nothing is overwritten or duplicated: every version stays readable. Provenance covers data and code: every table knows its parents and the code that made it. Change arrives by release: a dashboard stays on its version until you move it. In years of working this way, we haven't had a broken dashboard. Many hands, one history: teams work on the same data in parallel, the way they do on code. The same data gives the same results on any machine, at any site, with no copies to reconcile. Consuming data is easy: a couple of commands and read access. Open formats, so nothing is locked in, not even to datom.

And all of it with nothing to host: no server, no database, no infrastructure to maintain.

**16 · Where datom is not a good fit**

Where isn't datom a good fit? Some limits are by design. It isn't a database: there's no SQL engine, and it isn't built for transactional, write-heavy work. It's for analytics: tables written when data changes and read many times. Each table is processed in memory, so a single table should fit on a modern laptop, though a set can span far more. And tables are flat.

Other limits are for now. Writes are R only, and the Python reader is a preview. Data lives on a filesystem or S3, and code on GitHub, including Enterprise.

On validation: like any R package, it's risk-based and done by each adopter, for their intended use. datom runs inside your SCE, not in place of it.

**17 · What a standard invites** [2 clicks]

What ships today: versions, provenance, sets, access through the permissions your git host and storage already enforce, open formats, and a Python reader in preview. [click] Next, designed but not built: access computed from lineage, governance across projects including storage migration, and data products built on datom. [click] And open to anyone: other languages, other backends, EDC connectors, diffs between versions. The last slot is yours.

**18 · A standard gets better every time it's used**

A standard gets better every time it's used. So try it on your use case. Request a feature, or argue with the design. Build a reader or a connector. Pilot it with your team.

datom grew out of daapr, data as a product in R, and it's on CRAN today.

[advance] Thank you.
