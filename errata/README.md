# Chapter Errata

This page contains corrections and clarifications to the content found in the published book.

All code corrections listed on this page have been corrected in this repository.

## Chapter 2

### Page 43 - Breadboard Examples

**Incorrect Text**

The 3rd bullet point reads _"A2 is not electrically connected to B2 (they don't share the same row)."_. This statement is incorrect because A2 _is_ electrically connected to B2 because they do share the same row.

**Corrected Text**

The 3rd bullet point should be _"A2 is not electrically connected to **A3** (they don't share the same row)."_.


### Page 72 - poll_dweets_forever() function

There is a 4 space indentation missing in the code example for the function `poll_dweets_forever()` at line 13. The effect of this means the statement `sleep(delay_secs)` is outside the `while` block and the loop never incurs the delay. 

This error does not affect a readers ability to successfully run the example, but it does make the following paragraph describing line 13 practically incorrect as the code does not incur the 2-second delay mentioned.

The following image illustrates the issue.

![Code Example](./Chapter2Page72.png)