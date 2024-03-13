from shiny import ui

"""
This script lays out the UI for the survey landing page.
"""

intro_ui = ui.nav_panel(
    None,
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.h1(
                {"style": "text-align: center; font-size: 45px;"},
                ui.markdown("**Welcome to our study!**"),
            ),
            ui.br(),
            ui.div(
                {"style": "text-align: justify;"},
                ui.markdown(
                    "Thank you so much for participating in this brief survey"
                    + " to improve the understanding of human "
                    + "decision-making. This survey requests personal "
                    + "information limited to age, race, ethnicity, sex, and "
                    + "location. We estimate that this survey should take at "
                    + "most 1.5 minutes to complete.<br><br>"
                    + "Please read this page carefully and check the box at "
                    + "the bottom of the page if you agree to "
                    + "participate.<br><br>"
                    + "You must be 18 years old or older to participate.<hr>"
                    + "<h4>**Who we are**</h4>This study is conducted by "
                    + "researchers from Cornell University: Ian Lundberg, "
                    + "Jennah Gosciak, Elizabeth Moon, and "
                    + "Daniel Molitor.<br><br>"
                    + "<h4>**What the study is about**</h4>This survey aims "
                    + "to understand how individuals make decisions when "
                    + "choosing political candidates.<br><br>"
                    + "<h4>**What we will ask you to do**</h4>If you agree to "
                    + "participate, you will be asked to provide your "
                    + "preference for a candidate from two possible choices. "
                    + "You will be expected to read the information provided "
                    + "about each candidate, indicate your preference, answer "
                    + "a single multiple choice question about the content "
                    + "shown, and provide information on your age, race, "
                    + "ethnicity, sex, and location.<br><br>"
                    + "<h4>**Compensation**</h4>You will be compensated with "
                    + "a $0.50 monetary reward for participation "
                    + "in the survey.<br><br>"
                    + "<h4>**Risks**</h4>We anticipate that your "
                    + "participation in this survey presents no greater risk "
                    + "than everyday use of the Internet. However, if any of "
                    + "the survey questions cause you fatigue, discomfort, or "
                    + "upset, you are welcome to discontinue at any time and "
                    + "we encourage you to do so.<br><br>"
                    + "<h4>**Rights**</h4>Taking part in this study is "
                    + "completely voluntary. If you decide to participate, "
                    + "you are free to withdraw at any time for any reason. "
                    + "However, should you decide to withdraw, you will not "
                    + "be eligible for the $0.50 monetary reward.<br><br>"
                    + "<h4>**Benefits**</h4>There may be no direct or "
                    + "indirect benefit to you from participating in this "
                    + "study. However, the insights obtained from this "
                    + "research could lead to an improved understanding of "
                    + "the role individual preferences play in "
                    + "decision-making.<br><br>"
                    + "<h4>**Privacy**</h4>Your responses will be completely "
                    + "anonymous. We will not collect your name or any other "
                    + "personally identifiable information. Your responses "
                    + "will be anonymized and stored in an encrypted "
                    + "database. Only researchers involved in this study will "
                    + "have access to this information. De-identified data "
                    + "from this study may be shared with the research "
                    + "community at large to advance scientific knowledge. We "
                    + "will remove any personal information that could "
                    + "identify you before files are shared with other "
                    + "researchers to ensure that, by current scientific "
                    + "standards and known methods, no one will be able to "
                    + "identify you from the information we share.<br><br>"
                    + "<h4>**If you have questions about the study**</h4>You "
                    + "may contact the Cornell research team by emailing "
                    + "Ian Lundberg at ilundberg@cornell.edu or Jennah "
                    + "Gosciak at jrg377@cornell.edu. If you have concerns "
                    + "regarding your rights as a participant, you may "
                    + "contact the Institutional Review Board (IRB) for "
                    + "Human Participants at 607-255-5138 or access their "
                    + "website at http://www.irb.cornell.edu. You may also "
                    + "report your concerns or complaints anonymously through "
                    + "Ethicspoint online at www.hotline.cornell.edu or by "
                    + "calling toll free at 1-866-293-3077. Ethicspoint is "
                    + "an independent organization that serves as a liaison "
                    + "between the University and the person bringing the "
                    + "complaint so that anonymity can be ensured.<br><br>"
                    + 'If you agree to these conditions, please click "I '
                    + 'consent to participate" below. If you do not agree, '
                    + 'click the “I do not consent to participate” '
                    + "option.<br><br>"
                    + "By agreeing to participate, you confirm that you are "
                    + "over 18 years of age."
                )
            )
        ),
        ui.column(3)
    ),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.input_radio_buttons(
                id="consent",
                label="I have read the above information.",
                choices={
                    "consent_agree": "I consent to participate",
                    "consent_disagree": "I do not consent to participate",
                },
                selected="",
                width="100%",
            )
        )
    ),
    ui.row(
        ui.column(3),
        ui.column(
            6,
            ui.div(
                {"style": "text-align: right;"},
                ui.input_action_button("next_page_prolific_screening", "Next page \u27A4"),
            )
        ),
        ui.column(3)
    ),
    ui.br()
)
