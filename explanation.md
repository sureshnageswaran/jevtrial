# Test Case #1: final-certificate-requires-covenant-test

## The setup: a maintenance covenant loan

This loan isn't being monitored through collateral reports like an asset-based revolver. Instead, the lender is monitoring a **maintenance covenant**, a financial test that the borrower must satisfy on a recurring basis.

Think of it as a periodic health check. Every quarter, the borrower calculates a financial ratio defined in the credit agreement and certifies the result to the lenders. The lender's job is not simply to record the number. The lender must independently verify the calculation using the agreement's definitions and methodology.

---

## The metric: Total Net Leverage

The covenant in this agreement is **Total Net Leverage**, with a maximum permitted level of **6.0x**.

A simplified version of the calculation is:

> Total Debt minus permitted cash balances, divided by EBITDA.

The precise definition can become surprisingly technical. Credit agreements often contain detailed rules governing:

- Which debt counts
- How cash may be netted
- How acquisitions are treated
- EBITDA adjustments and add-backs
- Treatment of one-time expenses

That's why the agreement specifically notes that:

> "Total Net Leverage and permitted cash netting are defined in the executed agreement."

The covenant is therefore not simply a math problem. It is a contractual calculation.

---

## What happened

The borrower, **Meridian Components**, submitted its final quarterly compliance certificate on time.

The certificate reports:

- Quarter ended: September 30, 2026
- Reported Total Net Leverage: **5.8x**
- Covenant limit: **6.0x**

At first glance everything appears fine. The borrower is reporting compliance with roughly 0.2 turns of cushion.

However:

- The certificate has been received.
- The certificate is final.
- The calculation worksheet is available.
- There are no open reporting issues.
- There is no amendment or waiver.
- The analyst has **not yet performed the independent recalculation**.

That last fact is what drives the workflow.

---

## The question the test asks

### What should the monitoring team do next?

The answer is:

> **covenant_test**

Run the documented covenant calculation.

The policy is unusually explicit:

> "Run the documented covenant calculation when a final certificate reports a maintenance covenant metric."

The triggering condition has already occurred. A final compliance certificate has been received and contains a maintenance covenant calculation. The analyst therefore needs to perform the test.

---

## Why this is harder than it sounds

The reported number is below the covenant limit:

- Reported leverage: **5.8x**
- Maximum allowed: **6.0x**

Many models are tempted to stop there and conclude that no action is required.

That is exactly the trap.

The test is asking for the **next workflow step**, not the ultimate credit conclusion.

The borrower's figure has not yet been independently verified. Until the lender performs the contractual calculation, nobody actually knows whether the borrower is compliant.

A simple mistake in:

- Debt balances
- EBITDA adjustments
- Cash netting
- Quarter-end calculations

could change the outcome.

The policy therefore requires the calculation to be performed before any determination can be made.

---

## Why the other actions are wrong

### `no_action`

This is the most tempting incorrect answer.

The borrower says leverage is 5.8x, which appears compliant.

But the policy does not permit the analyst to accept the borrower's calculation without performing the documented test. The required workflow has not been completed.

---

### `credit_review`

A credit escalation would require a **verified** concern.

Nothing has been verified yet.

The borrower may be compliant. They may not be. The first step is to perform the calculation.

---

### `borrower_follow_up`

There is nothing missing.

The certificate has been received.

The worksheet is attached.

The metric is clearly reported.

The analyst already has the information needed to proceed.

---

### `counsel_review`

The case contains no legal ambiguity.

There is no dispute over definitions.

There is no waiver.

No default has been alleged.

No cure right has been asserted.

The agreement can simply be applied as written.

---

## A finance comparison

Suppose a public company reports quarterly earnings of **$1.25 per share**.

An equity analyst doesn't immediately publish:

> "The number is correct because management said so."

Instead, the analyst reviews the financial statements, rebuilds the model, and verifies the calculation.

This covenant test is the credit-monitoring equivalent of that process.

The borrower has provided the answer.

The lender's next job is to check the work.

---

## What the test is really evaluating

This test is less about leverage ratios and more about **workflow discipline**.

A weaker model often jumps directly to the conclusion:

> "5.8x is below 6.0x, therefore nothing is wrong."

A stronger model recognizes that:

1. A final certificate has been received.
2. The agreement requires a covenant calculation.
3. The analyst has not yet performed it.
4. Therefore the next action is **covenant_test**.

The model succeeds when it follows the process, not when it tries to predict the final outcome. Even though the borrower appears compliant, compliance has not yet been independently established, and the required calculation is precisely what the workflow is asking the analyst to perform.

# Test Case #2: missing-worksheet-requires-borrower-follow-up

## The setup: the certificate arrived, but the evidence did not

This case looks very similar to the previous one at first glance.

The borrower, **Meridian Components**, is subject to a quarterly maintenance leverage covenant. As required by the agreement, it submitted its compliance certificate.

However, a compliance certificate by itself is not enough.

The reported leverage ratio must be supported by detailed calculations showing how the borrower arrived at the number. In this case, those supporting schedules are missing.

Specifically, the package does not include:

- The EBITDA calculation
- The net debt calculation
- The supporting worksheets needed to reproduce the leverage ratio

As a result, the lender cannot independently verify the reported covenant result.

---

## Why the worksheet matters

Imagine a borrower reports:

> Total Net Leverage = 5.8x

That single number is the conclusion, not the calculation.

The lender still needs to understand:

- What debt balances were included
- What cash balances were netted
- What EBITDA adjustments were made
- Whether all calculations follow the agreement definitions

Without the supporting schedules, the reported ratio is essentially a black box.

The lender has the answer, but not the work showing how the answer was obtained.

---

## What happened

The facts are straightforward:

- The quarterly compliance certificate was received.
- The borrower submitted it through the normal reporting channel.
- The required supporting schedules were not attached.
- The analyst has not completed an independent recalculation.
- No prior request for the missing information is outstanding.
- No amendment, waiver, or reporting relief exists.

The document package is therefore incomplete.

---

## The question the test asks

### What should the monitoring team do next?

The answer is:

> **borrower_follow_up**

Request the missing schedules from the borrower.

The policy says:

> "Request missing, unclear, internally inconsistent, or late information needed to complete the test."

That is exactly the situation here.

The required information needed to perform the covenant test is missing, so the correct next step is to obtain it.

---

## Why this is harder than it sounds

Many models see two facts:

1. A compliance certificate has been received.
2. A covenant exists.

From there they jump directly to:

> covenant_test

That is a reasonable instinct, but it skips an important prerequisite.

The covenant test can only be performed when the required supporting information is available.

The policy states:

> "Run the documented covenant calculation when the required final certificate and supporting information are available."

The phrase **"and supporting information"** is doing all the work here.

The certificate alone is not sufficient.

Before the analyst can test compliance, the missing schedules must be obtained.

---

## Why the other actions are wrong

### `covenant_test`

This is the most tempting incorrect answer.

The analyst has the reported ratio, but does not have the underlying calculations.

Without the EBITDA schedule and net-debt schedule, the analyst cannot independently verify the number.

The prerequisite information is missing, so the test cannot yet be completed.

---

### `credit_review`

Nothing indicates a verified covenant breach or credit deterioration.

The issue is administrative, not credit-related.

The lender does not yet know whether the borrower is compliant or non-compliant because the supporting calculations have not been provided.

---

### `counsel_review`

There is no contractual dispute or legal question.

Nobody is challenging the covenant definition.

There is no waiver request.

There is no disagreement about interpretation.

The immediate issue is simply that part of the required reporting package is missing.

---

### `no_action`

The workflow is not complete.

A required component of the reporting package is absent, and the analyst cannot perform the covenant calculation.

Some action is necessary, making `no_action` incorrect.

---

## A finance comparison

Suppose a public company files an earnings release that says:

> EBITDA this quarter was $125 million.

But the detailed financial statements and supporting schedules are missing.

An analyst would not immediately validate the result and update their model.

The first step would be:

> "Please send the supporting schedules."

Only after receiving the underlying detail could the analyst verify the reported figure.

The same logic applies here.

The borrower has provided the headline covenant result, but not the evidence needed to support it.

---

## What the test is really evaluating

This test focuses on whether the model understands **workflow prerequisites**.

A weaker model recognizes that a covenant exists and immediately selects **covenant_test**.

A stronger model notices that the policy requires:

1. A final certificate.
2. Supporting information.
3. Then the covenant calculation.

Only the first requirement has been satisfied.

Because the required schedules are missing, the next action is not to perform the analysis. The next action is to obtain the information needed to perform the analysis.

That makes **borrower_follow_up** the correct answer.

# Test Case #3: verified-covenant-breach-requires-credit-review

## The setup: the calculation is finished

The previous covenant-monitoring cases were about gathering information and performing the required calculation.

This case begins after those steps have already been completed.

The borrower, **Meridian Components**, submitted its compliance certificate, the analyst obtained all required supporting information, and the covenant calculation was independently reperformed using the definitions in the executed credit agreement.

At this point, the workflow is no longer about collecting data or running calculations.

The question is what to do with the result.

---

## The metric: Total Net Leverage

The agreement contains a quarterly maintenance covenant requiring:

> Total Net Leverage ≤ 6.0x

After independently performing the calculation, the analyst arrives at:

> Total Net Leverage = 6.3x

That is not a close call or a preliminary estimate.

It is:

- Calculated using the agreement definitions.
- Independently checked.
- Verified through analyst reperformance.
- Subject to a completed second review.

In other words, the monitoring process has already done its job and produced a validated result.

---

## What happened

The facts are intentionally clean:

- The compliance certificate was received.
- The covenant calculation was completed.
- A second review was completed.
- The verified leverage ratio is 6.3x.
- The covenant limit is 6.0x.
- No waiver is recorded.
- No cure notice has been received.
- No amendment modifies the covenant.

The lender therefore has a verified covenant breach with no documented relief in place.

---

## The question the test asks

### What should the monitoring team do next?

The answer is:

> **credit_review**

The policy states:

> "Escalate a verified breach or policy-defined risk trigger to the credit team promptly."

That is exactly what has occurred.

The breach is no longer hypothetical.

It is no longer dependent on receiving information.

It is no longer awaiting calculation.

The calculation has been completed and the result has been verified.

Therefore the matter must be escalated to the credit team.

---

## Why this is harder than it sounds

Many models see the words:

> Covenant breach

and immediately jump to:

> counsel_review

or

> default assessment

Those actions sound reasonable because covenant breaches can ultimately raise legal and default-related questions.

But the test is asking for the **next workflow step**, not the final outcome.

The policy is explicit:

1. Verify the breach.
2. Escalate to credit.
3. Credit determines appropriate next actions.

The existence of a breach does not automatically mean the monitoring analyst should make legal determinations.

It means the analyst should route the matter to the group responsible for evaluating the credit implications.

---

## Why the other actions are wrong

### `covenant_test`

This action has already been completed.

The policy states that `covenant_test` is used when:

> "the agreement-defined calculation has not yet been completed."

In this case:

- The calculation is complete.
- The result is verified.
- A second review has been completed.

The workflow has already moved past this stage.

---

### `borrower_follow_up`

Nothing is missing.

The lender has:

- The certificate.
- The supporting information.
- The completed calculation.
- A verified result.

No additional borrower information is needed to establish whether the covenant was breached.

---

### `counsel_review`

This is one of the most tempting incorrect answers.

The agreement contains:

- An equity cure right.
- Potential notice requirements.
- Potential default implications.

However, the policy limits counsel review to situations involving legal interpretation or questions regarding notice, waiver, cure rights, or default status.

No such question has been raised yet.

The only established fact is that a verified covenant breach exists.

Under the policy, that fact is first escalated to credit.

If credit later needs legal guidance regarding cure rights, notice provisions, or enforcement matters, counsel may become involved at that stage.

---

### `no_action`

This is clearly incorrect.

A verified covenant breach is one of the most consequential outcomes that covenant monitoring can identify.

The policy specifically requires escalation when such a breach is confirmed.

Doing nothing would contradict the policy.

---

## A finance comparison

Imagine a bond analyst monitoring a company that is required to maintain certain leverage levels under its debt agreements.

If the analyst independently confirms that leverage exceeds the permitted threshold, they do not simply note it in a spreadsheet and move on.

Nor do they immediately declare a legal default.

Instead, they escalate the issue to the credit team responsible for evaluating:

- Severity
- Potential lender response
- Borrower outreach
- Waiver discussions
- Risk rating implications
- Reserve considerations

That is exactly what is happening here.

The monitoring function has discovered and validated an issue.

The credit function now needs to evaluate it.

---

## What the test is really evaluating

This test is about understanding the distinction between:

- **Detecting a problem**
- **Responding to a problem**

A weaker model often continues chasing earlier workflow steps:

> Maybe recalculate again.

Or it jumps to later-stage conclusions:

> Maybe this is a default.

A stronger model recognizes that the workflow has already established the key fact:

1. The covenant calculation was completed.
2. The result exceeded the contractual limit.
3. The breach was independently verified.
4. No cure, waiver, or amendment changes the result.
5. Policy requires escalation of verified breaches.

Therefore the correct next action is **credit_review**.

The test is essentially asking whether the model understands when an issue has moved from **analysis** into **credit-risk management**. Once the breach is verified, the analyst's job is no longer to prove it exists. The job is to escalate it to the team responsible for managing the resulting credit risk.

# Test Case #4: cash-netting-interpretation-question-to-counsel

## The setup: the numbers are known, but the rules are not

Most covenant-monitoring cases are about gathering information or performing calculations.

This case is different.

The analyst already has:

- The compliance certificate.
- The supporting account statements.
- The executed credit agreement.
- A completed covenant calculation.

The problem is not missing data.

The problem is determining how the agreement should be interpreted.

Specifically, the question is whether **$18 million of pledged cash** can be netted against debt when calculating Total Net Leverage.

---

## The covenant calculation depends on cash netting

Leverage ratios often permit the borrower to reduce debt by eligible cash balances.

In simplified terms:

> Net Debt = Total Debt − Eligible Cash

The logic is straightforward. A company with $500 million of debt and $100 million of unrestricted cash is generally in a better position than a company with $500 million of debt and no cash.

However, credit agreements rarely allow just any cash balance to be included.

The agreement usually imposes conditions regarding:

- Control of the account
- Accessibility of the funds
- Restrictions on use
- Existing liens or pledges
- Whether the cash is available to service debt

That distinction is exactly what matters here.

---

## What happened

The borrower included **$18 million of cash** in its leverage calculation.

Supporting documentation shows that this cash sits in an account that has been:

> pledged to a separate equipment lender.

The analyst then evaluated the impact of that cash balance.

The results are dramatically different depending on the interpretation:

| Scenario | Total Net Leverage |
|-----------|-----------|
| Include pledged cash | 5.9x |
| Exclude pledged cash | 6.2x |

The covenant limit is effectively sitting between those two outcomes.

That means the disputed cash balance is not a minor technical issue.

It determines whether the borrower passes or fails the covenant.

---

## The question the test asks

### What should the monitoring team do next?

The answer is:

> **counsel_review**

The policy states:

> "Refer a material question about interpreting agreement definitions or legal rights to counsel."

That is exactly the situation presented.

The issue is not whether the analyst can perform a calculation.

The analyst has already done that.

The issue is how the agreement should be interpreted when applied to a pledged cash account.

---

## Why this is harder than it sounds

Many models want to jump directly to one of two conclusions:

### Conclusion 1

> The borrower reported 5.9x, so they're compliant.

### Conclusion 2

> The analyst calculated 6.2x, so there's a breach.

Neither conclusion is justified.

The agreement definition itself is unclear.

The case specifically states:

> "The supplied clause does not clearly resolve this pledged-account fact pattern."

That sentence is doing most of the work in the test.

If the contract clearly allowed pledged cash to be netted, the analyst could proceed.

If the contract clearly prohibited pledged cash from being netted, the analyst could proceed.

But the agreement does neither.

The outcome depends on legal interpretation.

---

## Why the other actions are wrong

### `credit_review`

This is the most tempting incorrect answer.

The leverage ratio could be:

- 5.9x (compliant), or
- 6.2x (breach)

depending entirely on how the agreement is interpreted.

The policy says:

> "Escalate a verified breach."

No verified breach exists yet.

The very fact that determines whether a breach exists remains unresolved.

Escalating to credit would effectively force the credit team to make a legal interpretation that the policy has assigned elsewhere.

---

### `covenant_test`

The covenant calculation has already been performed.

The policy defines this action as appropriate when:

> "calculation inputs are clear and the documented calculation remains to be performed."

Neither condition applies.

The analyst has already completed the calculation, and the inputs are not clear because the eligibility of the cash balance is disputed.

---

### `borrower_follow_up`

Another tempting answer.

However, the policy reserves this action for situations where facts or evidence are missing.

That is not the problem here.

The analyst already knows:

- The amount of cash.
- The location of the cash.
- The existence of the pledge.
- The relevant agreement language.

The facts have been established.

The dispute concerns interpretation of those facts.

Asking the borrower for the same documents again does not resolve the contractual ambiguity.

---

### `no_action`

A material issue remains unresolved.

The disputed cash balance changes the covenant outcome and therefore requires further review.

Doing nothing would leave a potentially covenant-compliant borrower and a potentially covenant-breaching borrower in exactly the same status.

The policy clearly requires escalation.

---

## A finance comparison

Imagine an equity analyst reviewing a merger agreement.

The analyst has all the documents and all the numbers.

The problem is that a key clause can reasonably be read in two different ways, and each interpretation produces a dramatically different valuation.

The appropriate next step is not to pick whichever interpretation seems convenient.

The appropriate next step is to obtain legal guidance regarding what the agreement actually means.

This covenant-monitoring case is the credit equivalent of that situation.

The facts are known.

The contract is ambiguous.

The answer depends on interpretation.

---

## What the test is really evaluating

This test is designed to distinguish between:

- **Calculation questions**
- **Information-gathering questions**
- **Interpretation questions**

A weaker model focuses only on the numbers and chooses either:

- `credit_review` because 6.2x exceeds the covenant limit, or
- `no_action` because 5.9x is below the limit.

A stronger model recognizes that neither number can be relied upon until the underlying contractual question is resolved.

The workflow has already established the facts:

1. The certificate was received.
2. The account documentation was reviewed.
3. The calculation was reperformed.
4. The disputed cash item is material.
5. The agreement language does not clearly resolve the issue.

At that point, the problem ceases to be an accounting or credit question and becomes an interpretation question.

Because the policy directs material interpretation questions to legal review, the correct next action is **counsel_review**.

The test is fundamentally asking whether the model understands that ambiguity in a contract cannot be resolved by assumption. When the covenant outcome depends on a disputed interpretation of agreement language, the next step is to seek legal guidance before determining whether a breach exists.

# Test Case #5: superseded-metric-covered-by-executed-waiver-no-action

## The setup: a problem that has already been resolved

Many covenant-monitoring cases focus on discovering a problem.

This case focuses on recognizing when there is **no longer a problem**.

An automated monitoring feed surfaced a leverage ratio of **6.1x**, which would normally be concerning because the covenant limit is **6.0x**.

If that number were the operative result, the lender would likely need to investigate further.

The key issue in this case is that the 6.1x figure did **not** come from the final compliance package.

It came from a draft.

---

## Understanding draft versus final documents

In credit workflows, borrowers often prepare multiple versions of compliance certificates before submitting a final signed version.

Drafts may contain:

- Preliminary calculations
- Unreviewed adjustments
- Incorrect assumptions
- Numbers that later change during the close process

The lender monitors the final, executed reporting package, not earlier working versions.

A draft can be useful evidence, but once it is formally superseded, it is not the operative document.

In this case:

- A draft certificate showed leverage of **6.1x**.
- The final signed certificate shows **5.7x**.
- The final package has been independently verified.
- The draft has been formally marked as superseded.

The monitoring process therefore relies on the final certificate, not the draft.

---

## The additional fact: an executed waiver exists

Even more importantly, the lender's waiver repository shows that the leverage covenant was waived for this specific quarter.

The waiver has already been verified as:

- Executed by the required parties
- Effective for the relevant reporting period
- Applicable to the covenant under review

This means that even if there had been a covenant concern during the period, the lender has already documented formal relief.

The case is therefore resolved from both directions:

1. The final certificate reports compliance.
2. An effective waiver applies to the test period.

---

## What happened

The workflow facts are intentionally conclusive:

- The final certificate has been received.
- The final calculation was reperformed.
- The draft document has been marked superseded.
- The waiver has been independently verified.
- Any prior issue has been closed.
- No information requests remain outstanding.

The monitoring team has already completed the necessary work.

There is nothing unresolved.

---

## The question the test asks

### What should the monitoring team do next?

The answer is:

> **no_action**

The policy states:

> "Use when the flagged item is superseded or resolved, the operative facts are verified, and no follow-up remains."

That description matches this fact pattern almost word for word.

The item that triggered concern was a superseded draft value.

The operative facts have been verified.

The waiver has been confirmed.

No further action remains.

---

## Why this is harder than it sounds

Many models see only one fact:

> A leverage ratio of 6.1x appeared in the system.

From there, they often jump to:

> credit_review

or

> covenant_test

The test is designed to see whether the model can distinguish between:

- A currently relevant issue
- A historically observed but resolved issue

The existence of a concerning number somewhere in the record does not automatically create an active workflow obligation.

What matters is whether that number remains operative.

In this case it does not.

---

## Why the other actions are wrong

### `credit_review`

This is the most tempting incorrect answer.

A leverage ratio of 6.1x would normally exceed the covenant limit.

However:

- The ratio came from a superseded draft.
- The final certificate reports 5.7x.
- The waiver is effective for the period.
- The issue has already been closed.

There is no verified breach requiring escalation.

---

### `covenant_test`

The covenant-testing work has already been completed.

The workflow confirms:

- The final certificate was received.
- The final calculation was reperformed.

The policy uses `covenant_test` when the calculation still needs to be performed.

That is no longer true.

---

### `borrower_follow_up`

Nothing is missing.

The monitoring team already has:

- The final certificate
- Supporting documentation
- Verified calculations
- Verified waiver documentation

There is no outstanding information request.

---

### `counsel_review`

Counsel review would only be appropriate if the waiver's validity or effect were uncertain.

The case expressly states that:

- The waiver has been verified.
- It was properly executed.
- It is effective for the relevant test period.

No legal ambiguity remains.

---

## A finance comparison

Imagine an equity analyst receives an early earnings draft showing a company might miss expectations.

A week later:

- The final audited results are released.
- The company beats expectations.
- The earlier draft is formally withdrawn.

The analyst would not continue escalating concerns based on the obsolete draft.

The draft may remain part of the historical record, but it is not the operative result.

The same principle applies here.

The workflow follows the verified final documentation, not a superseded preliminary version.

---

## What the test is really evaluating

This test is designed to assess whether the model understands the concept of **operative facts**.

A weaker model reacts to the first concerning number it encounters:

> 6.1x exceeds 6.0x, therefore escalate.

A stronger model evaluates the entire decision context:

1. The concerning figure came from a draft.
2. The draft has been formally superseded.
3. The final signed certificate reports 5.7x.
4. The final calculation was independently verified.
5. An effective waiver covers the test period.
6. The prior issue has already been closed.
7. No documentation or analysis remains outstanding.

At that point, there is no remaining problem to solve.

The test is not asking whether a concerning number ever appeared in the process. It is asking whether any unresolved obligation still exists after all facts have been verified.

Because the flagged item has been superseded, the operative reporting is compliant, the waiver is effective, and all prior issues have been resolved, the correct action is **no_action**.



**Test Case #6: delayed-borrowing-base-certificate-requires-borrower-follow-up**

The setup: a loan whose size depends on the collateral

The borrower, Summit Industrial, has an asset-based revolver. It's a credit line like a corporate revolver, but how much they can draw isn't a fixed number. It depends on the value of their receivables and inventory.

The closest comparison is a margin account or a prime brokerage line. You can borrow against your positions, with a haircut on each one. Here the "positions" are receivables and inventory, and the haircuts are called advance rates, for example 85% of eligible receivables and 50% of inventory. The resulting borrowing limit is the borrowing base.

The certificate: the borrower marks its own collateral

The key difference from a margin account is that nobody marks the collateral to market each day. You can't look up a price for a company's receivables. Instead, the borrower sends a borrowing base certificate every month, which is a signed statement saying "here's our receivables and inventory, here's the calculation, here's how much we can borrow."

So for the lender, that certificate is the price feed. Until the next one arrives, they're lending against last month's numbers.

What happened

The October certificate was due October 31. It's now November 5, five days late. Nothing else is wrong: last month's certificate arrived, the borrower has no history of late reporting, nobody has asked them for it yet, and there's no waiver or default on record.

The question the test asks

▎ What should the monitoring team do first?

The answer is borrower_follow_up: contact the borrower and

Why this is harder than it sounds

The model chooses from 18 realistic middle-office actions. nsible responses to "collateral reporting is missing":

- Recalculate the borrowing base (covenant_test): you can'tcalculate with.
- Review the collateral (collateral_review) or consider reserves (reserve_analysis): same problem, there's nothing new to analyse.
- Escalate to credit (credit_review) or the risk committee e's no evidence the collateral has gotten worse. Thecertificate is just late, and treating that as a credit problem is an overreaction.
- Assess whether it's a default (default_assessment): that'rower has been asked and the facts are established.
- Log a reporting exception (reporting_exception): this is the subtle one. It's a valid step, but the policy says it comes after a request has gone unanswered, and no request has been sent yet.

In other words, all of these are reasonable things to do evuld come later in the process. The test checks whether themodel understands the order of steps, not just which actions relate to missing reporting.

A finance comparison: if a fund's monthly NAV statement doesn't show up, you don't mark the position down, call risk, or check whether the fund has
defaulted. You email the administrator and ask where it is.e answer.

What it showed in practice

In the first version of the test, the reporting_exception rd, so it technically fit the facts. Jev was split almost50/50, and Clef-flash picked it outright. Once the rule said it only applies after an unanswered request, both models chose borrower_follow_up. That's a useful point for your colleague too: in a benchmarhe policy rules is part of what you're testing, so anyambiguity there shows up directly in the scores.