# ME404 Syllabus

(Last Updated: Nov. 11, 2026)

## Instructor

Trevor T. Ashley (he/him), Adjunct Lecturer, Dept. Mechanical Engineering

**Email:** tashley@bu.edu

**About Me**: Trevor is a Senior Technical Staff in the Tactical Autonomy Group within the ISR and Tactical Systems
Division at MIT Lincoln Laboratory. Prior to his current role, he served as Technical Staff (2018-2022) and Assistant
Group Leader (2022-2025) within the Control and Autonomous Systems Group within the Engineering Division. Before joining
MIT Lincoln Laboratory, Trevor developed autonomy, guidance, navigation, and control algorithms for the SPUR robot at
QinetiQ North America. In 2016, he received the PhD degree in Mechanical Engineering from Boston University under the
direction of Sean B. Andersson; his graduate research focused on developing and testing novel control and estimation
algorithms for tracking fluorescent nanoparticles. Trevor was also the teaching fellow for ME404 in 2011 and continued
to drop in on future courses during his tenure as a graduate student. Additionally, Trevor worked at Electro Scientific
Industries, Inc., from 2009-2011 where he developed high-precision control algorithms for laser-based silicon
singulation equipment. Trevor's current research interests lie broadly in the area of perception-based guidance,
navigation, and control for multi-domain systems with a strong emphasis on establishing formal guarantees for
data-driven algorithms - especially those reliant on machine learning techniques.

## Meeting Time and Place

**Lectures:** Tuesday and Thursday, 3:30 - 5:15 PM, PHO 202

**Office Hours:**

- Tuesday and Thursday, 2:00 - 3:30 PM, EMA205 (2nd Floor, 730 Comm. Ave.)
- (As Requested) Tuesday and Thursday, 5:15 - 6:00 PM, PHO 202
- (As Requested) Email me and we'll find a time via Zoom or Google Meet

## Introduction and Course Goals

Systems and control theory plays a vital role across most aspects of modern life. Control systems are found in cars,
appliances, cell phones, airplanes, robots, and just about anywhere you look. The goal of this course is to introduce
you to the fundamental concepts in feedback control and provide you a set of tools to analyze and design controllers.
Our primary focus will be on what is known by the community as _classical control_, and topics will include: modeling,
feedback, transfer functions, frequency domain analysis and design (e.g., Bode and Nyquist plots), and PID control. Time
permitting, we'll cover elements from digital and state space control, which is how it’s (nearly) all done nowadays
anyway. My goal is to make the class as interactive as possible and to focus on the application and design of
controllers rather than (just) the theory and mathematics (but is still important, nonetheless).

## Course Prerequisites

All students should have taken **ME 302: Engineering Mechanics II**, as well as the standard math sequence. An
alternative name for our course very well could be "How to Do (Nearly) Anything with a Differential Equation", so you'll
want to make sure you've brushed up on your ordinary differential equations. (We'll do a short review at the start of
the semester.)

Helpful (but not required) prerequisites include a course on signals and systems (e.g., fourier series and transforms)
as well as complex variables (e.g., complex integration, Cauchy-Goursat theorem, residues).

In addition, MATLAB (including the Control System Toolbox) and Python will be used quite heavily. If you haven’t done so
already, you should download and install MATLAB and Python on your computer. Information on obtaining a copy of the
software can be found at:
[MATLAB](http://www.bu.edu/tech/support/research/software-and-programming/common-languages/matlab/) and
[Python](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/)

## Course Expectations and Grading

**Your overall grade will be assigned according to the following breakdown:**

- Class Participation (5%)
- Homework (25%)
- Midterm (30%)
- Final (40%)

### How to Succeed in this Course

Students enter this course with different backgrounds, strengths, and ways of approaching challenging material. No
single lecture can accommodate every student's individual learning needs. Consequently, the key to succeeding in this
course is simple: **take responsibility for your learning**.

The instructor and the student have different but complementary responsibilities. My responsibility is to create an
environment conducive to learning: to organize the material, explain difficult concepts, provide meaningful
opportunities for practice, offer constructive feedback, and answer questions. Your responsibility is to actively engage
with these opportunities and take ownership of developing your understanding.

In this course, understanding a concept means more than being able to reproduce the steps of a worked example. You
should be able to explain why a method works, recognize when it is applicable, and interpret the results in terms of the
physical system. For example, if you calculate the poles of a closed-loop system, you should be able to explain what
those poles imply about the system's behavior. If you cannot do that yet, you have identified something worth practicing
or asking about.

When preparing for an exam, don't ask yourself whether you understand the provided solutions. Ask yourself whether you
can solve the problems independently, without referring to the solutions. If you cannot, you have identified a gap in
your understanding. That gap is not a failure; it is an opportunity to focus your studying where it will be most
productive.

Although grades matter, particularly early in your career, they are ultimately an imperfect measure of what you know and
what you can do. The knowledge and skills you retain from this course will be more valuable in the long run than the
letter grade on your transcript. What is more important than grades is that you gain mastery of the skills presented in
this course so that you can _fluently_ leverage them in your future career. An _A_ grade indicates that you have
demonstrated to me that you have achieved a high level of proficiency with the concepts and techniques covered in this
course.

Control theory is a mathematical subject, but it is not merely a collection of mathematical techniques. The equations
describe the behavior of physical systems, and the goal is to develop the ability to reason about those systems. As you
study, continually ask yourself what the mathematics is telling you about the physics.

Put simply, the instructor can provide the kindling, demonstrate how to start a fire, and offer guidance when the flame
struggles to catch. But ultimately, it is the student who must put in the effort to ignite the fire, feed it, and keep
it burning. At the end of the semester, the instructor and student part ways, but the student is left with the fire
they've built. More importantly, they should leave knowing how to build and sustain a fire on their own.

I want every one of you to succeed in this course - not merely by earning a good grade, but by developing a genuine
understanding of control theory that you can carry into your future careers. Achieving that level of understanding takes
time, consistent effort, and a willingness to confront what you do not yet understand. I am committed to helping you get
there, but ultimately, the learning is yours to do. The more you invest in your education, the more you will take away
from it.

### Homework

Unless otherwise noted, homework will be graded for correctness and completeness. Homework will be due at the time
stated on the problem set. See the _AI Policy_ below.

### Midterm and Final Exam

The **midterm exam** will be held during our normal class period (3:30 - 5:15 PM) and location (PHO 202) on **November
5, 2026**.

The **final exam** will be held during 3:00 - 5:00 PM (note: this is _not_ our normal meeting time) in PHO 202 on
**December 17, 2026**.

## Artificial Intelligence Policy

I'll be direct and upfront about this: _you will use AI almost daily in your (future) career._ (I use it every day, even
to help me write lecture notes for this class.) Consequently, learning how to use AI effectively will now be one of your
greatest ongoing challenges, and you must maintain pace with technology that is developing at a nearly impossible rate.

> To leverage AI effectively, you must know when and how to trust the output of an AI agent. Completion of this course
> should enable you to understand how to assess the output of an AI agent when using it to design a control system.

Our AI policy for this course is as follows:

- **Problem Sets:**
  - Each problem set will have per-problem instructions regarding AI usage.
  - Before the problem set is turned in, you are not permitted to use AI to directly solve the problem for you.
    - <span style="color:green">OKAY:</span> "The book says this about gain and phase margin. Can you clarify what they
      mean by..."
    - <span style="color:green">OKAY:</span> "The book has this example problem. I don't understand how they derived ...
      . Can you explain it better?"
    - <span style="color:green">OKAY:</span> "How do I generally use lsim to simulate a dynamical system? What does
      ode45 actually do?"
    - <span style="color:red">NOT OKAY</span>: "Problem 2.45 is <...> . Solve the problem and provide me the solution.
      Show all work."
    - <span style="color:red">NOT OKAY</span>: "Here is my solution to Problem 2.45 <...>. Is it correct? If not,
      provide me a hint."
    - <span style="color:red">NOT OKAY</span>: "I'm stuck on Problem 2.45. Can you help me get unstuck?"
  - After the problem set is turned in, you are more than welcome _and encouraged_ to use AI to evaluate your solutions.
- **Exams:**
  - The midterm and final exams will not permit the use of AI. They will be closed-book and closed-notes, and you will
    be provided all the formulas you need to perform the exam.
- **Supplemental Problems:**
  - You are permitted _and encouraged_ to use AI while working on supplemental problems that will not be graded.
  - Caveat: AI can produce incorrect answers. You should not take the mindset that the agent is a knowledgeable
    professor who is concerned for your semester grade but rather a potentially malicious grad student who might trick
    you to see if you're actually paying attention.
  - I highly encourage you to use AI to create _visualizations_ of supplemental problems to help you connect with and
    explore the material. Much of control can feel very intuitive (e.g., PID tuning) after you see enough examples.

> If there's any doubt in when AI may or may not be permissible, please check with me. I'm generally liberal about AI
> use as long as it encourages and promotes your learning. On the other hand, I also encourage you to talk with your
> peers more than you do an AI agent. Please take responsibility for your learning.

## Textbook and References

### Primary Textbook

Our primary textbook will be:

> G. F. Franklin, J. D. Powell, and A. Emami-Naeini, _Feedback Control of Dynamic Systems_, 8th Edition, Prentice
> Hall, 2019.

(The sixth and seventh editions should also be ﬁne to use. The most recent 9th edition published by Pearson and authored
by Powell, Emami-Naeini, and Ivler may also suffice. You may just need to adjust the assigned reading if you deviate
from the 8th edition. Please talk to Trevor if there is any confusion.)

### Additional References

#### Classical Control

There are a number of textbooks on classical control, and they mostly carry the same content but provide different
exercises and perspectives on how to solve problems. I _highly_ recommend you supplement this course with this
additional material and work on exercises outside of our normal assigned homework. Talk to Trevor for recommendations.

- N. Nise, _Control Systems Engineering_, 8th Edtion, Wiley, 2019.
- K. Ogata, _Modern Control Engineering_, 5th Edition, Prentice Hall, 2009.
- R. C. Dorf, R. H. Bishop, _Modern Control Systems_, 14th Edition, Pearson, 2022.
- H. K. Khalil, _Control Systems: An Introduction_, 2023.
- K. J. Åström and R. M. Murray, _Feedback Systems: An Introduction for Scientists and Engineers_, Princeton University
  Press, 2021. [Available free online](https://www.cds.caltech.edu/~murray/FBS/Second_Edition.html)
- J. J. DiStefano, A. R. Stubberud, I. J. Williams, _Feedback and Control Systems_, 3rd Edition, McGraw Hill, 2014.
- S. Brunton, _Control Bootcamp_,
  [YouTube Link](https://www.youtube.com/watch?v=Pi7l8mMjYVE&list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m).
- B. Douglas, [YouTube Link](https://www.youtube.com/@BrianBDouglas/playlists).

#### Engineering Mathematics

During your career, you will quickly find that having an extensive and mature understanding of mathematics - both pure
and applied - will make you more useful and, to be honest, more employable. _Math is the language of engineering._ You
should continue to both broaden and deepen your understanding of mathematics, never becoming complacent. No worries -
there will _always_ be more to learn.

- E. Kreyszig, _Advanced Engineering Mathematics_, 10th Edition, Wiley, 2011.
- S. Brunton, _Engineering Math: Crash Course in Complex Analysis_,
  [YouTube Link](https://www.youtube.com/watch?v=_mv0q7-WF4E&list=PLMrJAkhIeNNQBRslPb7I0yTnES981R8Cg).
- S. Brunton, _Fourier Analysis_,
  [YouTube Link](https://www.youtube.com/watch?v=jNC0jxb0OxE&list=PLMrJAkhIeNNT_Xh3Oy0Y4LTj0Oxo8GqsC&pp=0gcJCf8COCosWNin).
- S. Brunton, _Differential Equations and Dynamical Systems_,
  [YouTube Link](https://www.youtube.com/watch?v=9fQkLQZe3u8&list=PLMrJAkhIeNNTYaOnVI3QpH7jgULnAmvPA&pp=0gcJCbwFa94AFGB0).

#### Signals and Systems

At most other universities, a course on signals and systems is a _required_ prerequisite to a course in control theory.
This textbook is considered a gold standard by many, and it should be a part of your bookshelf. A proper understanding
of Fourier series and transforms will help you better understand the nature of the Laplace transform as something more
than just an operator that "converts" a $t$ to an $s$.

- A. V. Oppenheim, A. S. Willsky, S. H. Nawab, _Signals & Systems_, 2nd Edition, Prentice Hall, 1997.

#### Control of Aerodynamic Systems

Many years ago, BU offered a sibling course to ME404 which was ME403: Control of Aerodynamic Systems. For those
interested in seeing controls as is usually taught from an aerodynamics perspective, I highly recommend this reference.

- R. F. Stengel, _Flight Dynamics_, 2nd Edition, Princeton University Press, 2022.

#### Data-driven Approaches

Machine learning and control theory go hand-in-hand, and techniques we learn from this course can enable you to better
understand machine learning techniques (e.g., gradient descent is a feedback loop!). Reinforcement learning is just
another way of implementing an optimal controller when modeling the system is challenging but numerically sampling from
it is easy. I highly recommend learning a bit about optimal control (see below) before tackling reinforcement learning.

- S. L. Brunton, J. N. Kutz, _Data-driven Science and Engineering: Machine Learning, Dynamical Systems, and Control_,
  2nd Edition, Cambridge University Press, 2022.
- R. S. Sutton, A. G. Barto, _Reinforcement Learning: An Introduction_, 2nd Edition, The MIT Press, 2018.
- S. L. Brunton, _Reinforcement Learning_,
  [YouTube Link](https://www.youtube.com/watch?v=0MNVhXEX9to&list=PLMrJAkhIeNNQe1JXNvaFvURxGY4gE9k74&pp=0gcJCf8COCosWNin).

#### Modern, Optimal, and Nonlinear Control

Through thought-leaders like Kalman, state-space methods led to a paradigm shift in the 1950s-1960s known as _modern
control_. These methods enable us to handle significantly more complex systems, including multi-input multi-output
systems, with relative ease. Moreover, all real-world systems are nonlinear, so having an understanding of the phenomena
they exhibit (e.g., bifurcations, finite escape times, chaos) will help you better understand how to control them.
Moreover, we often wonder when designing a control law, "Is this current control law _the best_ in some way?" The field
of optimal control will help you design feedback controllers that are _optimal_ (in some sense), leading to modern
approaches, like model predictive control, which is used in many modern applications like quadrotor racing.

- W. L. Brogan, _Modern Control Theory_, 3rd Edition, Prentice Hall, 1991.
- R.W. Brockett, _Finite Dimensional Linear Systems_, SIAM, 2015. (Book for ME501.)
- G. F. Franklin, J. D. Powell, M. L. Workman, _Digital Control of Dynamic Systems_, 3rd Edition, Addison-Wesley, 1998.
- S. Skogestad, I. Postlethwaite, _Multivariable Feedback Control: Analysis and Design_, 2nd Edition, Wiley, 2006.
- H.K. Khalil, _Nonlinear Systems_, Prentice-Hall, Third Edition, 2002. (Book for ME762.)
- D. Bertsekas, _Dynamic Programming and Optimal Control_, 4th Edition, Athena Scientific, 2020.
- A. E. Bryson, Y. Ho, _Applied Optimal Control_, Revised Printing, Taylor and Francis, 1975.
