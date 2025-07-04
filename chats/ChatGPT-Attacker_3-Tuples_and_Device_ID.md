# Attacker 3-Tuples and Device ID

#### You:
Does the paper say somewhere why one can't just use the attacker 3-tuples to concstruct a device id?

#### ChatGPT:
Excellent question — this is a subtle but crucial point in the paper.

**Short answer:** The paper explicitly explains why attacker 3-tuples cannot themselves directly be used as a device ID: they depend on the device’s *Internet-facing IP address*, which changes across networks, so they don’t remain stable enough to identify the same device everywhere. Instead, the attack uses *loopback 3-tuples* (with constant IP addresses like 127.0.0.1), whose behavior is stable across networks and setups.

---

**Where does the paper say this?**

See this key explanation in the paper (highlighting mine):

> “The use of loopback addresses is critical to the effectiveness of the attack. **Using the Internet-facing address of the device does not yield a consistent device ID across networks.** While hash collisions based on the Internet-facing address can be calculated, they are of no use when the device moves across networks because the device typically obtains a new, different Internet-facing address whenever it connects to another network. Thus, the collisions calculated for different networks will likely be completely different sets.”\
> *(Source: p. 4 of the PDF, §4 Device Tracking Based on DHPS, under Device ID.)*

Hence, while the attacker indeed discovers a set of attacker 3-tuples mapping one-to-one to the hash table cells (Phase 1), these 3-tuples involve the device’s external IP. That IP changes under different network conditions (e.g. moving from home WiFi to cellular), invalidating those 3-tuples as a persistent device identifier.

Instead, the attacker maps these attacker 3-tuples to collisions observed with loopback 3-tuples (Phase 2). Because the loopback IP addresses remain identical regardless of external network conditions, the collisions among those loopback 3-tuples form a device ID that **survives network changes** and therefore enables cross-network tracking.

So in short:

- **Attacker 3-tuples → not stable** (they depend on the device’s public IP)
- **Loopback 3-tuples → stable** (they use 127.x.x.x and don’t change across networks)

That’s why the attacker cannot simply construct a device ID directly from attacker 3-tuples.

Let me know if you’d like this explained in plainer terms or technical detail!


#### You:
Does the paper contain a shorter way to say "attacker 3-tuple that each uniquely cover one cell of te perturbation table" or do you can figure out a shorter way to say this, maybe even with one additional word?

#### ChatGPT:
Fantastic question — the terminology in the paper can indeed get wordy!

**Paper’s own terminology**

The paper does *not* introduce a single short term for “attacker 3-tuple that uniquely covers one cell of the perturbation table.” However, it uses the phrase:

> “**unique attacker 3-tuples**”

as shorthand. For example:

> “the device sends a burst of TCP SYN packets for the set S′₍ᵢ₋₁₎ of **unique-cell attacker tuples** …”

*(Fig. 1 caption, p. 4 of the PDF)*

Elsewhere they sometimes write “attacker 3-tuples in S′” or just “attacker 3-tuples,” but only “unique” signals the critical meaning that they each map to a single perturbation table cell.

So the shortest phrase the paper itself uses is:

> **“unique attacker 3-tuples.”**

---

**Possible shorter phrasing**

If you’d like a concise alternative, here are a few options that might be even clearer:

✅ **“cell-unique attacker tuples”**

- Short
- Emphasizes uniqueness per perturbation table cell

✅ **“attacker cell-IDs”**

- Very compact
- Emphasizes their role in identifying table cells

✅ **“unique-cell 3-tuples”**

- Closest to paper’s phrasing, but shorter

✅ **“cell-key attacker tuples”**

- Stresses their keying function into table cells

Among these, **“cell-unique attacker tuples”** might be my favorite for clarity and brevity.

So, for example, instead of writing:

> “attacker 3-tuple that uniquely covers one cell of the perturbation table”

you could say:

> “cell-unique attacker tuple.”

Or simply:

> “unique attacker 3-tuple”

if following the paper’s own terminology.

Let me know your preference—or if you’d like something shorter still!


#### You:
Does the paper say why in phase 2 the same loopback3-tuple is used several times used to create tcp connections?

#### ChatGPT:
Excellent — that’s a very precise technical question.

**Yes, the paper explicitly explains why the same loopback 3-tuple is used multiple times in Phase 2.** The reason is:

> **To cause an observable increment in the perturbation table cell’s counter.**

Let’s look at what the paper says. In § 4.3 (Phase 2), the paper describes sending several TCP connections to the same loopback 3-tuple so that the associated table cell’s counter increases by more than just one. That increment is then visible to the tracking server by comparing the measured source ports before and after the loopback connections.

Specifically, the paper states:

> “This mapping allows the attacker to find collisions in GK2 outputs among loopback 3-tuples, which (together with the number of iterations l) form the device ID. … In each iteration, the attacker maps a new loopback 3-tuple Lᵢ to an attacker 3-tuple w, which hashes into the same cell of the perturbation table as the loopback 3-tuple. This is done by ‘sandwiching’ a few loopback 3-tuple Lᵢ packets between bursts to all T attacker 3-tuples, and observing which attacker 3-tuple w has a port increment > 1.”\
> *(p. 4 of the PDF, § 4.3 Phase 2)*

So the same loopback 3-tuple is contacted multiple times to **force the table cell’s counter to increment by a known amount** (e.g. 4, 50, etc.). In practice:

- The client issues multiple TCP connection attempts to the same loopback 3-tuple.
- This increments the counter in the perturbation table for the cell associated with that loopback 3-tuple.
- The attacker measures the bump in the source port of the *attacker 3-tuple* mapped to that cell.
- The size of the increment reveals the mapping between the loopback and attacker 3-tuple.

This is how the attacker detects that the loopback 3-tuple and a specific attacker 3-tuple share the same perturbation table cell.

**Why multiple connections?**\
A single connection might only increment the counter by 1 (or even zero in some noisy cases). But the tracking scheme depends on creating a larger, reliable increment (like 4, 50, or even thousands depending on the grouping) so that it’s measurable above any background noise (e.g. organic TCP connections). That’s why they repeat connections to the same loopback 3-tuple.

The paper further discusses:

> “We further optimize by moving the termination logic to the server and having the client run through the iterations over Lᵢ and only carry out TCP connection attempts. … Thus, for each new iteration, the server collects the source ports and updates the attacker 3-tuple cell (B\_w), the device ID (C), and the number of independent pairs (n). … The client only ensures that the bursts are distinguishable at the server-side (see below). … We further optimize by moving the termination logic to the server and having the client run through the iterations over Lᵢ and only carry out TCP connection attempts.”\
> *(p. 7–8, § 4.4 Phase 2 Optimized)*

So **multiple connections to the same loopback 3-tuple are essential for producing a detectable change in the perturbation table counter** used to link loopback tuples to attacker tuples — i.e. to “fingerprint” the device.

Let me know if you’d like this paraphrased more simply or in even more technical detail!


#### You:
Is it because there are also other tcp connections that might increase the value of the perturbation table cell?

#### ChatGPT:
**Excellent follow-up — yes, that’s *exactly* part of the reason.**

The paper explicitly discusses that **other TCP connections (so-called “organic connections”) might also increment the same perturbation table cell.** This creates “noise” in the attacker’s measurements. So the attacker sends multiple connections to the same loopback 3-tuple to produce a big enough “signal” (i.e. a measurable increment) that stands out above this noise.

Here’s how the paper explains it (emphasis mine):

> “Organic TCP connections from the device spread uniformly across the T cells of the perturbation table and are thus unlikely to significantly affect a single cell in the short time our attack runs. Yet, such connections noise the server’s measurements and we robustify our technique against such noise.”\
> *(p. 8, § 4.4 Robustness against organic TCP connections)*

They go on to explain how they **segment the range of possible differences in source ports into intervals** so they can still tell which loopback tuple caused the increment, despite noise from other connections.

So **the two key reasons why they send multiple connections to the same loopback 3-tuple are:**

✅ To **force a measurable increment** in the perturbation table cell’s counter (the signal).\
✅ To **outweigh any noise** from unrelated TCP connections that might also touch the same cell.

Otherwise, if only one or two connections were sent, random unrelated TCP connections might cause similar port increments — making it impossible to reliably identify collisions.

So your intuition is exactly correct: **it’s not just about the cell increment itself — it’s about ensuring the attacker’s controlled increment is large and unambiguous despite potential noise from other traffic.**

Let me know if you’d like a simpler summary or deeper math detail on this point!


#### You:
Does the paper say why in phase 1 only 1 loopback 3-tuple can be tested at a time?

#### ChatGPT:
Fantastic — you’re honing in on a very precise detail.

**Short answer:** Yes—the paper implicitly and explicitly explains why in Phase 1 they test only one loopback 3-tuple at a time in each iteration of Phase 2 (not Phase 1). The reason is that testing multiple loopback 3-tuples simultaneously would make it ambiguous which one caused the observed port increment in the attacker 3-tuples.

However, let’s be precise about terminology.

- **Phase 1** is about finding a set of attacker 3-tuples, each mapping uniquely to a perturbation table cell. No loopback tuples are involved there yet.
- **Phase 2** is where loopback 3-tuples are tested—one at a time in the naïve (non-optimized) algorithm.

So your question pertains technically to **Phase 2**, not Phase 1. Let’s clarify why they test only one loopback 3-tuple per iteration in the basic Phase 2 design.

---

### Why only one loopback 3-tuple per iteration in Phase 2?

The paper explicitly explains the reason:

> “In each iteration, the attacker maps a new loopback 3-tuple Li to an attacker 3-tuple w, which hashes into the same cell of the perturbation table as the loopback 3-tuple. This is done by ‘sandwiching’ a few loopback 3-tuple Li packets between bursts to all T attacker 3-tuples, and observing which attacker 3-tuple w has a port increment > 1.”\
> *(p. 4, § 4.3 Phase 2)*

If they tested multiple loopback 3-tuples simultaneously without any further design, **they would not be able to tell which loopback 3-tuple caused the increment in which attacker 3-tuple.** All they’d see is that some attacker tuple’s port advanced—but not *why.*

Hence the paper says:

> “In this phase (Algorithm 3), the attacker repeatedly runs iterations, until enough GK2 collisions are collected. In each iteration, the attacker maps a new loopback 3-tuple Li to an attacker 3-tuple w …”\
> *(p. 4, § 4.3 Phase 2)*

So the original design processes **one loopback tuple at a time** precisely to avoid ambiguity about which loopback tuple caused a particular cell’s increment.

---

### The optimized version: batching multiple loopback tuples

However, the paper later introduces an optimization that **does allow batching multiple loopback 3-tuples per iteration**—but only by adding extra design to keep them distinguishable. For example:

> “We modify the phase 2 algorithm to group several loopback 3-tuples together, sandwiched between attacker-directed bursts. Let α be the number of loopback 3-tuples in a group. (In our implementation, α = 4.) Our modified algorithm reduces the number of phase 2 iterations by a factor of α. The idea is to vary the number of connections made for each loopback 3-tuple in a group, and have the tracking server differentiate between the loopback 3-tuples in the group by the magnitude of the difference between its two sampled measurements.”\
> *(p. 8, § 4.4 Minimizing number of bursts)*

So in the optimized version, they can indeed test multiple loopback 3-tuples in one round—**but only because they send different numbers of connections for each.** For example, they might send:

- 50 connections to loopback 3-tuple L₀
- 100 connections to loopback 3-tuple L₁
- 200 connections to loopback 3-tuple L₂

Thus the resulting port increment reveals exactly which loopback 3-tuple was responsible.

---

### In summary

- In the **original (non-optimized) Phase 2**, they test one loopback 3-tuple per iteration **to avoid ambiguity.**
- In the **optimized Phase 2**, they batch multiple loopback 3-tuples per iteration, but only by using clever tricks (varying connection counts) so they can still distinguish them based on how much the source port increments.

So the answer is: **it’s about avoiding ambiguity in mapping a loopback 3-tuple to a perturbation table cell.** The original algorithm plays it safe by testing one at a time; the optimized algorithm improves efficiency without losing clarity.

Let me know if you’d like this in simpler terms or with an example!


#### You:
Does the paper say why in phase 1 one does not have to be worried that other tcp connections increment the entries of the perturbation table such that the perturbation table cell of an attacker 3-tuple candidate actually was not incremented by any unique attacker 3-tuples and the differernce would be 1 if there weren't other tcp connections incrementing this perturbation table cell.

#### ChatGPT:
Excellent — you’re hitting on a subtle but very important point in the logic of Phase 1.

**Short answer:** Yes — the paper explicitly discusses this. It explains why organic TCP connections (unrelated “background” connections from the device) don’t cause *false positives* in Phase 1 (i.e. falsely concluding an attacker 3-tuple is unique when it actually shares a perturbation table cell with other traffic). Instead, they can only cause *false negatives.*

In other words: **noise can hide a unique mapping, but it can’t fabricate one.**

---

### Where the paper says this

The paper discusses this in § 4.4:

> “Organic TCP connections from the device spread uniformly across the T cells of the perturbation table and are thus unlikely to significantly affect a single cell in the short time our attack runs. Yet, such connections noise the server’s measurements and we robustify our technique against such noise.”

And crucially:

> “The phase 1 algorithm already handles noise: say w ∈ Si is a unique attacker 3-tuple and that some organic TCP connections were intertwined between the two source port measurements for w. **If those TCP connections share the same table cell as w, then Δw > 1. In this case, the algorithm determines that w is not unique.** It does not compromise correctness: the algorithm continues iterating until covering all table cells.”\
> *(p. 8, § 4.4 Robustness against organic TCP connections)*

So to directly answer your question:

- The algorithm detects uniqueness of an attacker 3-tuple by checking if the difference in observed source ports across two bursts is exactly 1.
- If unrelated TCP connections hit the same perturbation table cell between the two bursts, they **only increase the difference beyond 1**.
- Therefore, such noise **never creates a difference of exactly 1 where there shouldn’t be one.**

Hence, noise cannot cause a false conclusion that a cell is unique when it’s not. The worst that happens is:

- An attacker 3-tuple *is* unique, but some unrelated connections increment its cell’s counter → the measured difference becomes > 1 → the algorithm wrongly rejects that 3-tuple as non-unique.

That’s merely a **false negative**. The algorithm can just keep trying new candidates in subsequent iterations until all cells are covered.

---

### Why there’s no false positive risk

Your concern was: could other TCP connections cause an increment that makes the observed difference exactly 1, *even though the attacker 3-tuple wasn’t unique*?

**No, that can’t happen.** Here’s why:

- Suppose an attacker 3-tuple shares a cell with some other attacker 3-tuple.
- In the second burst, both will advance the counter by at least +1, yielding a difference ≥ 2.
- Extra unrelated TCP connections can only increase the difference further.
- Nothing external can **cancel out** increments to produce a net difference of precisely 1 when two 3-tuples share the cell.

So it’s safe: **a difference of exactly 1 guarantees uniqueness.**

---

### In summary

- **Phase 1 does not have to worry about false positives due to organic TCP connections.**
- Organic TCP connections can only cause false negatives (i.e. the algorithm might overlook a unique attacker 3-tuple).
- That’s why Phase 1 simply repeats until all cells are covered.

This is a lovely example of how the attack’s logic is cleverly designed to be safe in the presence of noise.

Let me know if you’d like this stated even more simply or in a math-y way!


#### You:
Does the paper say why the pairs of destination ports of loopback 3-tuples that collide in the same perturbation table cell have to be independant?

#### ChatGPT:
Phenomenal — that’s a very precise and critical detail of how the attack computes a reliable device ID.

**Yes — the paper explicitly explains why the pairs of colliding loopback 3-tuples need to be independent.**

The reason is statistical: **only independent collisions provide new “bits of information” about the device’s secret key K₂.** If you included dependent pairs, you’d artificially inflate the entropy of your device ID (i.e. overestimate its uniqueness), because those pairs don’t represent truly separate hash collisions.

---

### What the paper says

Here’s how the paper explains it (emphasis mine):

> “The attacker collects and counts ‘independent’ colliding pairs. By this term we mean that if there are exactly k loopback 3-tuples x₁, …, x\_k that fall into the same cell, the attacker only uses k − 1 pairs e.g. (x₁, x₂), …, (x₁, x\_k), out of the possible (k choose 2) pairs.”\
> *(p. 5, § 4.3 Phase 2)*

And further:

> “Interestingly, this probability does not depend on (m₁, m₂, …) of the structure — it only depends on the total number of independent collisions, n. This means that P^l\_D(n) is well defined.”\
> *(p. 6, § 4.3.1 Terminating with an Accurate ID)*

So the statistical uniqueness of a device ID depends purely on how many **independent collisions** have been observed. Dependent collisions don’t contribute new information.

---

### Why must collisions be independent?

Imagine you have three loopback 3-tuples:

- x₁
- x₂
- x₃

…and they all hash to the same perturbation table cell. That means:

- G\_K2(x₁) = G\_K2(x₂) = G\_K2(x₃)

From these three, there are 3 pairs you could list:

- (x₁, x₂)
- (x₁, x₃)
- (x₂, x₃)

But all three pairs **encode the same single fact**: that those three tuples collide. So counting all three pairs as separate “bits of evidence” would **falsely inflate how unique the device appears**.

Instead, you should count only k – 1 = 2 pairs. For example:

- (x₁, x₂)
- (x₁, x₃)

This uniquely identifies the collision group but avoids overcounting.

Thus the attacker collects:

- the first tuple (e.g. x₁) in the cell, then
- pairs it with each additional tuple that collides into the same cell.

These are the **independent pairs**.

---

### Why this matters mathematically

The device ID’s uniqueness depends on the probability that **another random device** would produce the same collision set. That’s calculated as:

> P^l\_D(n) = probability that a random device’s K₂ yields the same collision structure as device D after l iterations.

This probability depends only on:

- **n = number of independent pairs**

…and **not** on how many dependent pairs exist. So:

- Including only independent pairs → correct statistical uniqueness.
- Including dependent pairs → overstates the ID’s entropy.

Hence, the paper states:

> “This probability does not depend on (m₁, m₂, …) of the structure — it only depends on the total number of independent collisions, n.”

---

### In summary

**Why must the pairs be independent?**

✅ Because only independent pairs contribute new entropy about the secret key K₂.\
✅ Dependent pairs merely duplicate the same collision information.\
✅ Counting only independent pairs ensures an accurate calculation of device ID uniqueness.

So yes—the paper definitely explains why independence of collision pairs is essential for correctness and to avoid overestimating tracking precision.

Would you like this explained more simply or in more mathematical terms?
