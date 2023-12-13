# Qualtrics for Adaptive Experiments

I have recently reached out to the Cornell Qualtrics team to investigate
the possibility of setting up an action that dynamically responds to
each survey response so that we can adaptively run our code pipeline on
each new response. Although the Qualtrics API does have this
functionality, it is limited to individuals with the "Brand Ambassador"
role. Since we are licensed under Cornell's organizational license, this
means that there is a single Brand Ambassador for all Qualtrics users on
the Cornell account. Unsurprisingly, this means that no Cornell
Qualtrics users are allowed to access features that are restricted to
Brand Ambassadors. **TLDR**: We are SOL.

My interpretation of this is, as long as we are fine with manually
downloading batches of responses on Qualtrics, we are fine to keep hosting
the survey on Qualtrics. However, if we want to estimate stuff adaptively,
we will have to implement our own survey.

To see the full details of this exchange,
[see this PDF](qualtrics-service-request.pdf).