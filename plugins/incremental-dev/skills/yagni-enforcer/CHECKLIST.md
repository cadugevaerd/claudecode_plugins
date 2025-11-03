# YAGNI Checklist

**Step-by-step checklists for detecting and preventing over-engineering.**

## ✅ YAGNI Checklist for Code Review

### For Each File:

````text

[ ] Abstract classes have 3+ implementations?
    ❌ Less than 3 → REMOVE abstraction

[ ] Factory creates 3+ different types?
    ❌ Only 1-2 → USE direct creation

[ ] Pattern used in 3+ contexts?
    ❌ Only 1-2 → SIMPLIFY to function

[ ] Configuration manages 10+ values?
    ❌ Less than 10 → USE dict/constants

[ ] Function has 3+ parameters used?
    ❌ Unused parameters → REMOVE

[ ] Class has state that varies?
    ❌ Stateless → USE function

[ ] Code used in last 3 months?
    ❌ Not used → DELETE

[ ] Complexity justified by real requirement?
    ❌ Anticipated complexity → SIMPLIFY

```text


## 📋 Pre-Implementation Checklist

Before implementing a feature, ask yourself:

```text

YAGNI PRE-IMPLEMENTATION CHECKLIST:

[ ] Is this needed RIGHT NOW?
    ❌ No → DON'T implement it yet

[ ] What breaks if I DON'T implement this?
    ❌ Nothing breaks → Probably not needed

[ ] Does this solve the MINIMUM problem?
    ❌ No → Remove unnecessary parts

[ ] Am I using "for the future" language?
    ❌ Yes → RED FLAG - Reconsider

[ ] Am I creating abstraction with < 3 cases?
    ❌ Yes → DON'T create abstraction

[ ] Am I hardcoding in MVP?
    ✅ Yes → GOOD! Configuration comes later

[ ] Can I implement this in < 2 hours?
    ❌ No → Probably over-engineered

[ ] Will this complexity help the CURRENT user?
    ❌ No → Remove it

```text


## 🔍 Detection Checklist - When Adding Features

**Use this when you're about to add a feature:**

```text

ADDING A NEW FEATURE - YAGNI CHECK:

1. WHAT AM I ADDING?
   [ ] New function/method
   [ ] New class
   [ ] New parameter
   [ ] New configuration
   [ ] New pattern/abstraction

2. DO I NEED THIS NOW?
   [ ] Current user requires it? (YES = good)
   [ ] Anticipated future need? (NO = YAGNI!)
   [ ] Solving current problem? (YES = good)

3. HOW MANY PLACES USE THIS?
   [ ] 1 place → Inline or direct
   [ ] 2 places → Duplication is OK
   [ ] 3+ places → NOW abstract/refactor

4. IS THIS COMPLEX?
   [ ] Simple (< 5 lines)? → Keep it
   [ ] Medium (5-20 lines)? → Is it needed?
   [ ] Complex (20+ lines)? → RED FLAG

5. CAN I SIMPLIFY THIS?
   [ ] Remove parameters? → Do it
   [ ] Hardcode values? → Do it in MVP
   [ ] Use built-in? → Do it
   [ ] Remove class? → Make it function

6. AVOID RED FLAGS:
   [ ] "For the future" language?
   [ ] Preparing for expansion?
   [ ] "To facilitate..."?
   [ ] Clean architecture patterns?
   All ✅ (none) → Good to add!

```text


## 🚨 Red Flag Detection - Phrases to Watch

**If you hear/use these phrases - QUESTION IT:**

```text

RED FLAG PHRASES:

❌ "Let's prepare for the future..."
❌ "In case we need to..."
❌ "To facilitate expansion..."
❌ "Following clean architecture..."
❌ "For flexibility..."
❌ "To allow for..."
❌ "Leaving room for..."
❌ "Anticipating..."
❌ "Just to be safe..."
❌ "It might be useful..."

✅ INSTEAD USE:

✅ "Let's make it work first"
✅ "We'll add this when necessary"
✅ "Focus on current use case"
✅ "We'll refactor when pattern emerges"
✅ "Delete if not used"
✅ "Simple and direct"
✅ "Solve NOW, not future"

```text


## 📊 Checklist: Rule of 3

**Before creating abstraction, verify you have 3+ cases:**

```text

RULE OF 3 VERIFICATION:

Feature/Pattern: ____________________

Count implementations/usages:
[ ] 1st occurrence - Location: _________
[ ] 2nd occurrence - Location: _________
[ ] 3rd occurrence - Location: _________
[ ] 4th+ occurrences - Found? (Y/N)

DECISION:
[ ] < 3 cases → DO NOT ABSTRACT
[ ] 3+ cases → Safe to abstract
[ ] Exact duplicate? (Y/N) → Note differences
[ ] Pattern clear? (Y/N) → Proceed with abstraction

```text


## 🏗️ Architecture Complexity Checklist

**When designing architecture, verify it's necessary:**

```text

ARCHITECTURE COMPLEXITY CHECK:

[ ] Do we have 10+ classes?
    ❌ No → Architecture likely over-engineered

[ ] Do we have 3+ levels of inheritance?
    ❌ Yes → Probably over-engineered

[ ] Do we have 5+ design patterns?
    ❌ Yes → RED FLAG

[ ] Is configuration > 50 lines?
    ❌ Yes → Simplify

[ ] Do we need 3+ abstraction layers?
    ❌ Yes → Flatten

[ ] Can a junior dev understand in 30 min?
    ❌ No → Too complex

VERDICT:
[ ] Simple architecture ✅
[ ] Over-engineered ❌ (simplify!)

```text


## 💻 Code Smell Checklist

**Run this when reviewing code:**

```text

CODE SMELL DETECTION:

[ ] Abstract class with 1 implementation?
    → REMOVE abstraction

[ ] Factory that creates 1 type?
    → Use direct creation

[ ] 3+ functions doing similar thing?
    → Candidate for refactoring

[ ] Configuration object with < 10 values?
    → Use dict/constants

[ ] Class without state?
    → Make it function

[ ] Function with 5+ parameters?
    → Consider if all needed

[ ] Import that's not used?
    → Remove

[ ] Function longer than 50 lines?
    → Possibly too complex

[ ] "TODO" comment with no deadline?
    → Maybe feature creep

[ ] Validation more complex than feature?
    → Simplify

[ ] Configuration more complex than feature?
    → Use hardcoding in MVP

VERDICT:
[ ] No smells ✅
[ ] Some smells (refactor) ⚠️
[ ] Many smells (over-engineered) ❌

```text


## 📝 Post-Increment Checklist

**After completing each increment, verify:**

```text

POST-INCREMENT YAGNI CHECK:

[ ] Code compiles/runs without error?
[ ] Functionality works as needed?
[ ] Old code still works?
[ ] No unused code added?
[ ] No abstractions with < 3 cases?
[ ] No "future-proofing" code?
[ ] Can new code be understood in 2 min?
[ ] Increment size reasonable (< 2 hours)?
[ ] All parameters/config actually used?
[ ] No unnecessary classes/patterns?

RESULT:
[ ] All clear ✅ → Commit
[ ] Issues found ❌ → Simplify and retry

```text


## 🎯 MVP Specific Checklist

**When working on MVP, verify:**

```text

MVP YAGNI CHECKLIST:

[ ] NO abstract classes?
[ ] NO design patterns?
[ ] NO sophisticated error handling?
[ ] NO complex validation?
[ ] NO premature optimization?
[ ] Hardcoded configuration OK? ✅
[ ] Simple functions, not classes?
[ ] Direct calls, not factories?
[ ] Readable, not beautiful?
[ ] Working, not perfect?

RESULT:
[ ] MVP simple ✅
[ ] Over-engineered MVP ❌ (simplify!)

```text


## 🔄 When to Refactor Checklist

**Only refactor when ALL conditions are met:**

```text

REFACTORING DECISION CHECKLIST:

[ ] Clear pattern emerged (3+ cases)?
    ❌ No → Wait

[ ] Duplication is obvious?
    ❌ No → Maybe not needed

[ ] Cost < 2 hours?
    ❌ No → Too complex to refactor now

[ ] Benefit > Cost?
    ❌ No → Skip refactoring

[ ] Already have tests?
    ❌ No → Add tests first

[ ] Safe to refactor (low risk)?
    ❌ No → Wait for more stability

DECISION:
[ ] All ✅ → REFACTOR
[ ] Any ❌ → WAIT

```text


**Use these checklists proactively to prevent over-engineering!**
````
